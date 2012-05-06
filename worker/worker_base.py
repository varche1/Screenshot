<<<<<<< HEAD
# -*- coding: utf-8 -*-
import os
import sys
import random
import base64

from selenium import selenium
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from urlparse import urlparse
from urllib2 import Request, urlopen, URLError, HTTPError

import pymongo
import gridfs
from pymongo.errors import ConnectionFailure, PyMongoError
from gridfs.errors import GridFSError
from bson import BSON
from bson.objectid import ObjectId

from PIL import Image

from celery.task import task
from celery.execute import send_task
from celery.loaders.default import Loader
from celery.exceptions import RetryTaskError, MaxRetriesExceededError

# logging errors
def on_failure_handler(self, exc, task_id, args, kwargs, einfo):
    logger = self.get_logger(loglevel="ERROR", logfile="localWorkerErrors.log")
    logger.error("Worker error: \n\tOS - {0} \n\tException: {1}".format(sys.platform, exc))

#@task(ignore_result=True)
def getScreenMain(rowId, pageUrl, pageId, browser, resolution, socket_id):
    try:
        config = Loader().read_configuration()
        
        fileName = getScreenImage(pageUrl, browser, resolution)
        
        thumbnailImageData = ResizeImage(fileName,
            (config["SCREENSHOT_THUMB_SIZE"]["width"],
            config["SCREENSHOT_THUMB_SIZE"]["height"]))
        mediumImageData = ResizeImage(fileName,
            (config["SCREENSHOT_MEDIUM_SIZE"]["width"],
            config["SCREENSHOT_MEDIUM_SIZE"]["height"]))
        originalImageData = ResizeImage(fileName,
            (config["SCREENSHOT_ORIGINAL_SIZE"]["width"],
            config["SCREENSHOT_ORIGINAL_SIZE"]["width"]))
        
        connection = pymongo.Connection(
            config["CELERY_MONGODB_BACKEND_SETTINGS"]["host"],
            config["CELERY_MONGODB_BACKEND_SETTINGS"]["port"])
        db = connection.screener
        
        data = {
            'ready': 1,
            'image' : {
                'thumbnail': BSON.encode({'data': base64.b64encode(thumbImageData)}),
                'medium': BSON.encode({'data': base64.b64encode(mediumImageData)}),
                'original': BSON.encode({'data': base64.b64encode(originalImageData)})
            }
        }
        
        db.screen.update({'_id': ObjectId(rowId)}, {'$set': data})
        
        return {'resolution' : resolution, 'page' : pageId, 'browser' : browser, '_id' : rowId, 'socket_id' : socket_id}

    except ConnectionFailure, e:
        raise Exception("Error while connecting to MongoDB: {0}.".format(str(e)))
    except PyMongoError, e:
        raise Exception("Error while working with MongoDB: {0}.".format(str(e)))
    except Exception, e:
        raise Exception(str(e))
    finally:
        if 'connection' in locals(): 
            connection.disconnect()
        
        # removing temporary file    
        if 'fileName' in locals(): 
            try:
                os.remove(fileName);
            except IOError, e:
                raise Exception("Error while removing original screenshot(temporary file): {0}.".format(str(e)))

#@task(ignore_result=True)
def getScreenImage(url, browser, resolution):
    try:
        # cheking URL
        url = urlparse(url)
        if not (url.netloc and url.scheme):
            raise Exception("URL {0} is malformed.".format(url.geturl()))

        checkedRequest = Request(url.geturl())
        checkedRequest.get_method = lambda : 'HEAD'
        try:
            response = urlopen(checkedRequest)
            response.info().gettype()
        except HTTPError, e:
            raise Exception("URL {0} is unreachable: {1}.".format(url.geturl(), str(e)))
        except URLError, e:
            raise Exception("URL {0} is malformed: {1}.".format(url.geturl(), str(e)))

        # cheking resolution
        try:
            res = [int(x) for x in resolution.split('_')]
        except:
            raise Exception("Resolution {0} is malformed.".format(resolution))
        
        if (not (len(res) == 2 and res[0] > 0 and res[1] > 0)):
            raise Exception("Resolution {0} is malformed.".format(resolution))
        
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
                raise Exception("Browser\'s name {0} is malformed.".format(browser))
        except Exception, e:
            raise Exception("Browser initialization error: {0}.".format(str(e)))
        
        # preparing browser
        driver.set_window_size(res[0], res[1])
        driver.get(url.geturl())
        
        # taking screenshot
        fileName = '{0}_{1}.jpeg'.format(random.randrange(1, 99999), random.randrange(1, 99999))
        if (not(driver.get_screenshot_as_file(fileName))):
            raise Exception("Error while taking/saving screenshot: (Browser) - {0}, (URL) - {1}, (File Name) - {2}.".format(driver.name, driver.current_url, fileName))
        
        driver.close()
        
        return fileName
    
    except  WebDriverException, e:
        raise Exception("Browser\'s error: {0}.".format(str(e)))
    except Exception, e:
        raise Exception(str(e))

#@task(ignore_result=True)
def ResizeImage(fileNameOrig, size):
    try:
        config = Loader().read_configuration()
        
        # checking size
        if (size <= 0):
            raise Exception("Size {0} is malformed.".format(size))
        
        # opening image
        try:
            image = Image.open(fileNameOrig)
        except IOError, e:
            raise Exception("Error while opening original screenshot: {0}.".format(str(e)))
        
        # resizing image    
        iSize = image.size   
        try:
            if (size[0]):
                resImage = image.resize((size[0], int(iSize[1] / (float(iSize[0]) / size[0]) )), Image.ANTIALIAS)
        except Exception, e:
            raise Exception("Error while resizing original screenshot: (Size) - {0}, (Error) - {1}.".format(size, str(e)))    
        
        # croping image   
        try:    
            if (size[1]):
                resImage = resImage.crop((0, 0, size[0], size[1]))
        except Exception, e:
            raise Exception("Error while croping original screenshot: (Size) - {0}, (Error) - {1}.".format(size, str(e)))    
        
        return resImage.tostring('jpeg', quality=config["SCREENSHOT_QUALITY"])
    
    except Exception, e:
        raise Exception(str(e))
