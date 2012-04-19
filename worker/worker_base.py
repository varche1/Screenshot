# -*- coding: utf-8 -*-
import os
import random

from selenium import selenium
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from urlparse import urlparse
from urllib2 import Request, urlopen, URLError, HTTPError

import pymongo
import gridfs
from pymongo.errors import ConnectionFailure, PyMongoError
from gridfs.errors import GridFSError

from PIL import Image

from celery.task import task
from celery.execute import send_task

# logging errors
def on_failure_handler(self, exc, task_id, args, kwargs, einfo):
    logger = getScreenMain.get_logger(loglevel="ERROR", logfile="localWorkerErrors.log")
    logger.error("Worker error: \n\tOS - {0} \n\tException: {1}".format(os.uname(), exc))

@task(ignore_result=True)
def getScreenMain(rowId, pageUrl, pageId, browser, resolution, socket_id):
    try:
        fileName = getScreenImage(pageUrl, browser, resolution)
        
        thumbImageData  = ResizeImage(fileName, (100, 100))
        normalImageData = ResizeImage(fileName, (1000, 0))
        
        connection = pymongo.Connection('176.9.24.81', 27017)
        db = connection.screener
        fs = gridfs.GridFS(db)
        
        fs.put(thumbImageData,  filename=rowId+"thumb")
        fs.put(normalImageData, filename=rowId+"normal")
        
        result = [socket_id, resolution, pageId, browser, rowId]
        
        # server notification about complite task
        send_task("server.response_action", result, queue="response_q")
        
        return { 'state' : "COMPLITE-getScreen", 'rowId' : rowId }
    
    except ConnectionFailure, e:
        raise Exception("Error while connecting to MongoDB: {0}.".format(str(e)))
    except GridFSError, e:
        raise Exception("Error while putting file to MongoDB: (rowId) - {0}, (Error) - {1}.".format(rowId, str(e)))
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

@task(ignore_result=True)
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

@task(ignore_result=True)
def ResizeImage(fileNameOrig, size):
    try:
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
            resImage = image.resize((size[0], int(iSize[1] / (float(iSize[0]) / size[0]) )), Image.ANTIALIAS)
        except Exception, e:
            raise Exception("Error while resizing original screenshot: (Size) - {0}, (Error) - {1}.".format(size, str(e)))    
        
        # croping image   
        try:    
            if (size[1]):
                resImage = resImage.crop((0, 0, size[0], size[1]))
        except Exception, e:
            raise Exception("Error while croping original screenshot: (Size) - {0}, (Error) - {1}.".format(size, str(e)))    
         
        # saving image     
        fileName = '{0}_{1}.jpeg'.format(random.randrange(1, 99999), random.randrange(1, 99999))
        try:
            resImage.save(fileName, "JPEG", quality=85)
        except IOError, e:
            raise Exception("Error while saving resized screenshot: {0}.".format(str(e)))
        
        # opening resized image to the memory
        try:
            resultFile = open(fileName, "rb")
            data = resultFile.read();
            resultFile.close();
        except IOError, e:
            raise Exception("Error while opening resized screenshot: {0}.".format(str(e)))
            
        return data;
    
    except Exception, e:
        raise Exception(str(e))
    finally:
        if 'fileName' in locals():
            
            # removing temporary file
            try:
                os.remove(fileName);
            except IOError, e:
                raise Exception("Error while removing resized screenshot(temporary file): {0}.".format(str(e)))
                
