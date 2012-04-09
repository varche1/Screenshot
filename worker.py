import StringIO
from base64 import decodestring
from urlparse import urlparse

from selenium import selenium
from selenium import webdriver

import pymongo
import gridfs

from PIL import Image


def getScreen(rowId, pageUrl, browser, resolution):
    
    image = getScreenImage(pageUrl, browser, resolution)
    if (image is None):
        return
    
    thumbImageData  = ResizeImage(image, (100, 100))
    normalImageData = ResizeImage(image, (1000, 0))

    db = pymongo.Connection('localhost', 27017).screener
    fs = gridfs.GridFS(db)
    
    fs.put(thumbImageData,  filename=rowId+"thumb")
    fs.put(normalImageData, filename=rowId+"normal")


def getScreenImage(url, browser, resolution):
    url = urlparce(url)
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
    imgB64 = driver.get_screenshot_as_base64()
    driver.close()
    
    imgIOString = StringIO.StringIO(decodestring(imgB64))
    image = Image.open(imgIOString)
    imgIOString.close()
    return image


def ResizeImage(image, size):
    iSize = image.size
    resImage = image.resize((size[0], int(iSize[1] / (float(iSize[0]) / size[0]) )), Image.ANTIALIAS)
    if (size[1]):
        resImage = resImage.crop((0, 0, size[0], size[1]))
    
    imgIOString = StringIO.StringIO()
    resImage.save(imgIOString, "JPEG", quality=85)
    data = imgIOString.getvalue()
    imgIOString.close()
    return data