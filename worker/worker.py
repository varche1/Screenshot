# -*- coding: utf-8 -*-
import worker_base
import sys
from urllib2 import urlopen, HTTPError,URLError
from celery.task import task
from celery.loaders.default import Loader
from celery.exceptions import RetryTaskError, MaxRetriesExceededError, SoftTimeLimitExceeded

@task(on_failure = worker_base.on_failure_handler, max_retries=3, default_retry_delay=10)
def getScreen(rowId, pageUrl, pageId, browser, resolution, socket_id):
    try:
        return worker_base.getScreenMain(rowId, pageUrl, pageId, browser, resolution, socket_id)
    except RetryTaskError, e:
        pass
    except MaxRetriesExceededError, e:
        pass
    except SoftTimeLimitExceeded, e:
         raise Exception(str(e))
    except Exception, e:
        getScreen.retry(exc=e)
    
@task(on_failure = worker_base.on_failure_handler)
def updateWorker(reason):    
    try:
        config = Loader().read_configuration()
        
        # update base_worker
        response = urlopen(config['BASE_WORKER_URL'])
        
        wFile = open(config['BASE_WORKER_MODULE'], 'w')
        wFile.write(response.read())
        wFile.close()
        
        # update celery config
        response = urlopen(config['CELERYCONFIG_URL'])
        
        wFile = open(config['CELERYCONFIG_MODULE'], 'w')
        wFile.write(response.read())
        wFile.close()
        
        #reboot system
        if sys.platform == 'win32':
            try:
                import win32api
                win32api.InitiateSystemShutdown(None, '', 0, True, True)
            except ImportError:
                raise Exception("Can not reboot system. pywin32 not found")
        
        else:
            import os
            os.system('reboot now')
        
    except (HTTPError,URLError), e:
        raise Exception("Can not get source file from GitHub: {1}.".format(str(e)))
    except IOError, e:
            raise Exception("Error saving source file: {0}.".format(str(e)))
    except Exception, e:
        raise Exception("Error while updating: {0}.".format(str(e)))