# -*- coding: utf-8 -*-
from daemon import Daemon

import tornado.ioloop
import tornado.web
import tornado.template
import tornado.escape

import sys, os
import json

import pymongo, gridfs
from bson.objectid import ObjectId

 #Распределенные задачи
from celery.task import task
from celery.execute import send_task
from celery.task.sets import subtask
from celery.task.sets import TaskSet

APP_DIR = os.path.dirname(os.path.abspath(__file__))

class CoreHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.db         = database
        self.arguments  = {k : v[0] for k,v in self.request.arguments.items()}
        try:
            self.data = {k : v for k,v in json.loads(self.request.body).items()}
        except:
            self.data = {}
    
    def response(self, message, code, status):
        self.write({'success': status, 'code': code, 'results': message})
    
    def objectIdToStr(self, row):
        if (type(row) is dict):
            row['_id'] = str(row['_id'])
        else:
            row = str(row)
        return row
    
    def strToObjectId(self, strId):
        return ObjectId(str(strId))
    
    def writeToDB(self, table, isInsert=False):
        itemId = self.data.pop('_id')
        if (isInsert is True):
            itemId = self.db[table].insert(self.data)
        else:
            self.db[table].update({'_id': self.strToObjectId(itemId) }, {'$set': self.data})
        self.data.update({'_id': str(itemId)})


class MainHandler(CoreHandler):
    
    def get(self):
        loader = tornado.template.Loader(os.path.join(APP_DIR, 'templates'))
        self.write(loader.load("index.html").generate())


class SitesHandler(CoreHandler):
    
    table = 'sites'
    
    def get(self):
        self.response([self.objectIdToStr(item) for item in self.db[self.table].find()], 0, True)
    
    def put(self):
        if 'url' and 'title' not in self.data:
            return self.response("arguments not found", 10, False)
        
        self.writeToDB(self.table, True);
        self.response(self.data, 0, True)

    def post(self):
        if 'url' and 'title' not in self.data:
            return self.response("arguments not found", 10, False)
        
        self.writeToDB(self.table);
        self.response(self.data, 0, True)
    
    def delete(self):
        self.db.sites.remove({'_id': self.strToObjectId(self.data['_id'])})
        self.response(None, 0, True)


class PagesHandler(SitesHandler):
    
    table = 'pages'
    
    def get(self):
        if 'site' not in self.arguments:
            return self.response("arguments not found", 10, False)
        
        res = [self.objectIdToStr(item) for item in self.db[self.table].find({'site': self.arguments['site']})]
        self.response(res, 0, True)


class ScreenHandler(CoreHandler):
    
    def get(self):
        if 'page' not in self.arguments:
            return self.response("arguments not found", 10, False)
        
        res = [self.objectIdToStr(item) for item in self.db.screen.find({'page': self.arguments['page']})]
        self.response(res, 0, True)
    
    def put(self):
        if 'url' and 'title' and 'site' not in self.data:
            return self.response("arguments not found", 10, False)
        
        self.data.pop('_id')
        
        itemId = self.db.pages.insert(self.data)
        self.data.update({'_id': str(itemId)})
        self.response(self.data, 0, True)

    def post(self):
        if 'browsers' and 'pages' and 'resolution' not in self.data:
            return self.response("arguments not found", 10, False)
        
        for k,v in self.data.items():
            if (type(v) is not list):
                self.data[k] = [v]
        
        for pageId in self.data['pages']:
            page = self.db.pages.find_one({'_id': self.strToObjectId(pageId)})
            if (not page): continue
            
            for browserId in self.data['browsers']:
                system, browser, version = browserId.split('_')
                
                for resolutionId in self.data['resolution']:
                    screen = self.db.screen.find_one({'page': pageId, 'browser': browserId, 'resolution': resolutionId})
                    if (screen):
                        rowId = screen['_id']
                    else:
                        rowId = self.db.screen.insert({'page': pageId, 'browser': browserId, 'resolution': resolutionId})
                    
                    addTask(self.objectIdToStr(rowId), page['url'], system, browser, resolutionId)
        
        self.response({}, 0, True)


class ImageHandler(CoreHandler):
    
    def get(self):
        if 'page' and 'type' not in self.arguments:
            return self.response("arguments not found", 10, False)
        
        
        fs = gridfs.GridFS(self.db)
        try:
            image = fs.get_version(self.arguments['page'] + self.arguments['type'])
            self.set_header("Content-Type", 'image/jpeg')
            self.write(image.read())
        except:
            raise tornado.web.HTTPError(404)


@task
def addTask(rowId, pageUrl, system, browser, resolutionId):
    """
    смотрим system (win7, winxp, ubuntu)
    и создаем задачу в нужном потоке
    """
    
    # опции для задачи
    options = [rowId, pageUrl, browser, resolutionId]
    
    # очередь, куда отправлять задачу, будет название OS - system
    #send_task("worker.get_screen", options, queue=system)
    send_task("worker.getScreen", options)


connection = pymongo.Connection('127.0.0.1', 27017)
database = connection.screener

application = tornado.web.Application([
    (r"/",              MainHandler, dict(database=database)),
    (r"/site",          SitesHandler, dict(database=database)),
    (r"/page",          PagesHandler, dict(database=database)),
    (r"/screen",        ScreenHandler, dict(database=database)),
    (r"/image",         ImageHandler, dict(database=database)),
    (r"/static/(.*)",   tornado.web.StaticFileHandler, {"path": os.path.join(APP_DIR, 'static')}),
    (r"/get-worker",    tornado.web.StaticFileHandler, {"path": os.path.join(APP_DIR, 'worker'), 'default_filename': 'worker.py'}),
])

class TornadoDaemon(Daemon):
    def run(self):
        application.listen(80)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":

    pid_file = os.path.join(APP_DIR, 'tornado.pid')
    log_file = os.path.join(APP_DIR, 'logs', 'tornado.log')    

    daemon = TornadoDaemon(pid_file, stdout=log_file, stderr=log_file)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
    