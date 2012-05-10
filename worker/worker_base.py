# -*- coding: utf-8 -*-
#test autoreload
import os
import sys
import random
import base64

from urlparse import urlparse
from urllib2 import Request, urlopen, URLError, HTTPError

from selenium import selenium
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

import pymongo
from pymongo.errors import ConnectionFailure, PyMongoError
import bson
from bson.objectid import ObjectId

from PIL import Image, ImageOps
from StringIO import StringIO

from celery.task import task
from celery.execute import send_task
from celery.loaders.default import Loader
from celery.exceptions import RetryTaskError, MaxRetriesExceededError

# logging errors
def on_failure_handler(self, exc, task_id, args, kwargs, einfo):
    logger = self.get_logger(loglevel="ERROR", logfile="localWorkerErrors.log")
    logger.error("Worker error: \n\tOS - %s \n\tException: %s" % (sys.platform, exc))

def getScreenMain(rowId, pageUrl, pageId, browser, resolution, socket_id):
    try:
        config = Loader().read_configuration()
        
        screenData = getScreenImage(pageUrl, browser, resolution)
        
        thumbnailImageData = ResizeImage(screenData,
            (config["SCREENSHOT_THUMB_SIZE"]["width"], config["SCREENSHOT_THUMB_SIZE"]["height"]))
        mediumImageData = ResizeImage(screenData,
            (config["SCREENSHOT_MEDIUM_SIZE"]["width"], config["SCREENSHOT_MEDIUM_SIZE"]["height"]))
        originalImageData = ResizeImage(screenData,
            (config["SCREENSHOT_ORIGINAL_SIZE"]["width"], config["SCREENSHOT_ORIGINAL_SIZE"]["width"]))
        
        connection = pymongo.Connection(
            config["CELERY_MONGODB_BACKEND_SETTINGS"]["host"],
            config["CELERY_MONGODB_BACKEND_SETTINGS"]["port"])
        db = connection.screener
        
        updateData = {
            'ready': 1,
            'images.thumbnail': bson.binary.Binary(thumbnailImageData),
            'images.medium': bson.binary.Binary(mediumImageData),
            'images.original': bson.binary.Binary(originalImageData)
        }
        db.screen.update({'_id': ObjectId(rowId)}, {'$set': updateData})
        
        return {'resolution' : resolution, 'page' : pageId, 'browser' : browser, '_id' : rowId, 'socket_id' : socket_id}

    except ConnectionFailure, e:
        raise Exception("Error while connecting to MongoDB: %s." % str(e))
    except PyMongoError, e:
        raise Exception("Error while working with MongoDB: %s." % str(e))
    except Exception, e:
        raise Exception(str(e))
    finally:
        if 'connection' in locals(): 
            connection.disconnect()

def getScreenImage(url, browser, resolution):
    try:
        # cheking URL
        url = urlparse(url)
        if not (url.netloc and url.scheme):
            raise Exception("URL %s is malformed." % url.geturl())

        checkedRequest = Request(url.geturl())
        checkedRequest.get_method = lambda : 'HEAD'
        try:
            response = urlopen(checkedRequest)
            response.info().gettype()
        except HTTPError, e:
            raise Exception("URL %s is unreachable: %s." % (url.geturl(), str(e)))
        except URLError, e:
            raise Exception("URL %s is malformed: %s." % (url.geturl(), str(e)))

        # cheking resolution
        try:
            res = [int(x) for x in resolution.split('_')]
        except:
            raise Exception("Resolution %s is malformed." % resolution)
        
        if (not (len(res) == 2 and res[0] > 0 and res[1] > 0)):
            raise Exception("Resolution %s is malformed." % resolution)
        
        try:
            # cheking browser
            if (browser == 'ff'):
                driver = webdriver.Firefox()
            
            elif (browser == 'ch'):
                driver = webdriver.Chrome()
            
            elif (browser == 'ie'):
                driver = webdriver.Ie()
            
            elif (browser == 'op'):
                driver = webdriver.Opera()
            
            else:
                raise Exception("Browser\'s name %s is malformed." % str(e))
        except Exception, e:
            raise Exception("Browser initialization error: %s." % str(e))
        
        # preparing browser
        driver.set_window_size(res[0], res[1])
        driver.get(url.geturl())
        
        # taking data of screenshot
        screenB64 = driver.get_screenshot_as_base64()
        driver.close()
        if not screenB64:
            raise Exception("Screenshot doesn't get")
        
        return base64.decodestring(screenB64)
    
    except  WebDriverException, e:
        raise Exception("Browser\'s error: %s." % str(e))
    except Exception, e:
        raise Exception(str(e))

def ResizeImage(screenData, size):
    try:
        config = Loader().read_configuration()
        
        # checking size
        if (size <= 0):
            raise Exception("Size %s is malformed." % size)
        
        # opening image
        try:
            image = Image.open(StringIO(screenData))
        except IOError, e:
            raise Exception("Error while opening original screenshot: %s." % str(e))
        
        # resizing image    
        try:
            if (size[1]):
                resImage = ImageOps.fit(image, (size[0], size[1]), Image.ANTIALIAS)
            
            elif (size[0]):
                iSize = image.size
                resImage = image.resize((size[0], int(iSize[1] / (float(iSize[0]) / size[0]) )), Image.ANTIALIAS)
            
            else:
                resImage = image
            
        except Exception, e:
            raise Exception("Error while resizing original screenshot: (Size) - %s, (Error) - %s." % (size, str(e)))
        
        # get image data
        FileIOStr = StringIO()
        resImage.save(FileIOStr, "JPEG", quality=95)
        
        data = FileIOStr.getvalue()
        FileIOStr.close()
        
        return data
    
    except Exception, e:
        raise Exception(str(e))
