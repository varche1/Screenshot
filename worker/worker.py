# -*- coding: utf-8 -*-
import worker_base

from celery.task import task

@task
def getScreen(rowId, pageUrl, browser, resolution):
    #logger = getScreen.get_logger(loglevel="ERROR", logfile="fatalErrors.log")
    #logger.error("Start task: %s" % ("getScreen"))
    
    return worker_base.getScreenMain(rowId, pageUrl, browser, resolution)
