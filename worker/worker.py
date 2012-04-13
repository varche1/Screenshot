# -*- coding: utf-8 -*-
import os

from urlparse import urlparse
import random

from selenium import selenium
from selenium import webdriver

import pymongo
import gridfs

from PIL import Image

from celery.task import task
from celery.execute import send_task
from celery.task.sets import subtask
from celery.task.sets import TaskSet

@task
def getScreen(rowId, pageUrl, browser, resolution):
    fileName = getScreenImage(pageUrl, browser, resolution)
    if (fileName is None):
        return
    
    thumbImageData  = ResizeImage(fileName, (100, 100))
    normalImageData = ResizeImage(fileName, (1000, 0))
    
    db = pymongo.Connection('176.9.24.81', 27017).screener
    fs = gridfs.GridFS(db)
    
    fs.put(thumbImageData,  filename=rowId+"thumb")
    fs.put(normalImageData, filename=rowId+"normal")
    
    # remove temp file
    os.remove(fileName);
    
    # answer
    result = rowId
    
    send_task("server.response_action", [result], queue="response_q")
    
    return "COMPLITE - getScreen"

def getScreenImage(url, browser, resolution):
    url = urlparse(url)
    if not (url.netloc and url.scheme):
        return None
    
    try:
        res = [int(x) for x in resolution.split('_')]
    except:
        return None
    
    if (not (len(res) == 2 and res[0] > 0 and res[1] > 0)):
        return None
    
    if (browser == 'ff'):
        driver = webdriver.Firefox()
    
    elif (browser == 'ch'):
        driver = webdriver.Chrome()
    
    elif (browser == 'ie'):
        driver = webdriver.Ie()
    
    elif (browser == 'op'):
        driver = webdriver.OperaDriver()
    
    else:
        return None
    
    driver.set_window_size(res[0], res[1])
    driver.get(url.geturl())
    fileName = '{0}_{1}.jpeg'.format(random.randrange(1, 99999), random.randrange(1, 99999))
    driver.get_screenshot_as_file(fileName)
    driver.close()
    
    return fileName


def ResizeImage(fileNameOrig, size):
    image = Image.open(fileNameOrig)
    iSize = image.size
    resImage = image.resize((size[0], int(iSize[1] / (float(iSize[0]) / size[0]) )), Image.ANTIALIAS)
    if (size[1]):
        resImage = resImage.crop((0, 0, size[0], size[1]))
        
    fileName = '{0}_{1}.jpeg'.format(random.randrange(1, 99999), random.randrange(1, 99999))
    resImage.save(fileName, "JPEG", quality=85)
    
    resultFile = open(fileName, "rb")
    data = resultFile.read();
    resultFile.close();
    
    # remove temp file
    os.remove(fileName);
    
    return data;