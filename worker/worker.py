# -*- coding: utf-8 -*-
import os
import sys
import worker_base
from urllib2 import urlopen, HTTPError,URLError
from celery.task import task
from celery.loaders.default import Loader
from celery.exceptions import RetryTaskError, MaxRetriesExceededError, SoftTimeLimitExceeded

# Loading libraries needed to restart celery process
import subprocess
try:
    import signal
except ImportError:
    signal = None

# logging errors
def on_failure_handler(self, exc, task_id, args, kwargs, einfo):
    logger = self.get_logger(loglevel="ERROR", logfile="localWorkerErrors.log")
    logger.error("Worker error: \n\tOS - %s \n\tException: %s" % (sys.platform, exc))

@task(on_failure = on_failure_handler)
def getScreen(*args, **kwargs):
    return worker_base.getScreenMain(*args, **kwargs)

@task(on_failure = on_failure_handler)
def updateWorker(reason):    
    try:
        config = Loader().read_configuration()
        
        # update base_worker
        
        for F in config['UPDATE_FILES']:
            response = urlopen(F['url'])
            if not response:
                continue
            updFile = open(os.path.join(config['ROOT_WORKER_FOLDER'], F['file']), 'w')
            updFile.write(response.read())
            updFile.close()
        
        # reload process
        _reload()
        
    except (HTTPError,URLError), e:
        raise Exception("Can not get source file from GitHub: {1}.".format(str(e)))
    except IOError, e:
            raise Exception("Error saving source file: {0}.".format(str(e)))
    except Exception, e:
        raise Exception("Error while updating: {0}.".format(str(e)))

# Reload pocess. Copy from tornado.autoreload
def _reload():
    if hasattr(signal, "setitimer"):
        # Clear the alarm signal set by
        # ioloop.set_blocking_log_threshold so it doesn't fire
        # after the exec.
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
    if sys.platform == 'win32':
        # os.execv is broken on Windows and can't properly parse command line
        # arguments and executable name if they contain whitespaces. subprocess
        # fixes that behavior.
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit(0)
    else:
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except OSError:
            # Mac OS X versions prior to 10.6 do not support execv in
            # a process that contains multiple threads.  Instead of
            # re-executing in the current process, start a new one
            # and cause the current process to exit.  This isn't
            # ideal since the new process is detached from the parent
            # terminal and thus cannot easily be killed with ctrl-C,
            # but it's better than not being able to autoreload at
            # all.
            # Unfortunately the errno returned in this case does not
            # appear to be consistent, so we can't easily check for
            # this error specifically.
            os.spawnv(os.P_NOWAIT, sys.executable,
                      [sys.executable] + sys.argv)
            sys.exit(0)