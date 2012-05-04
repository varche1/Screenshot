# -*- coding: utf-8 -*-
import worker_base
from urllib2 import urlopen, HTTPError,URLError
from celery.task import task

@task(on_failure = worker_base.on_failure_handler)
def getScreen(rowId, pageUrl, pageId, browser, resolution, socket_id):    
    return worker_base.getScreenMain(rowId, pageUrl, pageId, browser, resolution, socket_id)
    
@task(on_failure = worker_base.on_failure_handler)
def updateWorker(reason):    
    try:
        response = urlopen('https://raw.github.com/varche1/Screenshot/master/worker/worker_base.py')
        
        wFile = open('worker_base.py', 'w')
        wFile.write(response.read())
        wFile.close()
    except (HTTPError,URLError), e:
        raise Exception("Can not get source file from GitHub: {1}.".format(str(e)))
    except IOError, e:
            raise Exception("Error saving source file: {0}.".format(str(e)))
    except Exception, e:
        raise Exception("Error while updating: {0}.".format(str(e)))
