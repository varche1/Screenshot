# -*- coding: utf-8 -*-
import worker_base
from celery.task import task

@task(on_failure = worker_base.on_failure_handler)
def getScreen(rowId, pageUrl, pageId, browser, resolution, socket_id):    
    return worker_base.getScreenMain(rowId, pageUrl, pageId, browser, resolution, socket_id)
