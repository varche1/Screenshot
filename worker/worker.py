# -*- coding: utf-8 -*-
import worker_base
from celery.task import task

@task(on_failure = worker_base.on_failure_handler)
def getScreen(rowId, pageUrl, browser, resolution):    
    return worker_base.getScreenMain(rowId, pageUrl, browser, resolution)
