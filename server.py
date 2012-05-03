# -*- coding: utf-8 -*-
from daemon import Daemon

import tornado.ioloop
import tornado.web
import tornado.template
import tornado.escape
import tornado.gen
from tornado import websocket
import tornado.options

from configuration import ScreenshotConfigs

import sys, os
import json
import uuid
import logging

import pymongo, gridfs
import asyncmongo

from bson.objectid import ObjectId

 #Распределенные задачи
from celery.task import task
from celery.execute import send_task

# temp
import time

APP_DIR = os.path.dirname(os.path.abspath(__file__))

class CoreHandler(tornado.web.RequestHandler):
    """
    Корневой класс. Содержин базовые методы приложения
    """
    
    def initialize(self):
        # Перегоняем request-аргументы в список
        self.arguments  = {k : v[0] for k,v in self.request.arguments.items()}
        try:
            self.data = {k : v for k,v in json.loads(self.request.body).items()}
        except:
            self.data = {}
    
    def getMongoResult(self, result):
        if (result[1]['error'] is not None or result[0][0]):
            pass
            #TODO rise Error
        
        result = result[0][0]
        if isinstance(result, list) and len(result) == 1:
            return result[0]
        
        return result
    
    # Шаблон стандартного ответа
    def response(self, message, code, status):
        self.write({'success': status, 'code': code, 'results': message})
        self.finish()
    
    def objectIdToStr(self, row):
        if (type(row) is dict):
            row['_id'] = str(row['_id'])
        else:
            row = str(row)
        return row
    
    def strToObjectId(self, strId):
        return ObjectId(str(strId))
    
    @property
    def db(self):
        return self.application.db
    
    @property
    def wsPool(self):
        return self.application.webSocketsPool
    
    @property
    def tasksPool(self):
        return self.application.tasksPool


class MainHandler(CoreHandler):
    
    def get(self):
        configs = ScreenshotConfigs()
        mongo_conf = configs.GiveMongoConnectionConf()
        
        loader = tornado.template.Loader(os.path.join(APP_DIR, 'templates'))
        self.set_cookie('socket_id', str(uuid.uuid4()))
        self.write(loader.load("index.html").generate(mongo_conf = mongo_conf))


class SitesHandler(CoreHandler):
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        response = yield tornado.gen.Task(self.db.sites.find)
        result = self.getMongoResult(response)
        self.response([self.objectIdToStr(item) for item in result], 0, True)
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def put(self):
        if 'url' and 'title' not in self.data:
            self.response("arguments not found", 10, False)
            return
        
        response = yield tornado.gen.Task(self.db.sites.insert, self.data)
        result = self.getMongoResult(response)
        
        self.response(self.data, 0, True)
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        if 'url' and 'title' and '_id' not in self.data:
            self.response("arguments not found", 10, False)
            return
        
        itemId = self.data.pop('_id')
        
        response = yield tornado.gen.Task(self.db.sites.update, {'_id': self.strToObjectId(itemId) }, {'$set': self.data})
        result = self.getMongoResult(response)
        
        self.response(self.data, 0, True)
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def delete(self):
        if '_id' not in self.data:
            self.response("arguments not found", 10, False)
            return
        
        response = yield tornado.gen.Task(self.db.sites.remove, {'_id': self.strToObjectId(self.data['_id'])})
        result = self.getMongoResult(response)
        
        self.response(None, 0, True)


class PagesHandler(SitesHandler):
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        if 'site' not in self.arguments:
            self.response("arguments not found", 10, False)
            return
        
        response = yield tornado.gen.Task(self.db.pages.find, {'site': self.arguments['site']})
        result = self.getMongoResult(response)
        
        self.response([self.objectIdToStr(item) for item in result], 0, True)
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def put(self):
        if 'url' and 'title' not in self.data:
            self.response("arguments not found", 10, False)
            return
        
        response = yield tornado.gen.Task(self.db.pages.insert, self.data)
        result = self.getMongoResult(response)
        
        self.response(self.data, 0, True)
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        if 'url' and 'title' and '_id' not in self.data:
            self.response("arguments not found", 10, False)
            return
        
        itemId = self.data.pop('_id')
        
        response = yield tornado.gen.Task(self.db.pages.update, {'_id': self.strToObjectId(itemId) }, {'$set': self.data})
        result = self.getMongoResult(response)
        
        self.response(self.data, 0, True)
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def delete(self):
        if '_id' not in self.data:
            self.response("arguments not found", 10, False)
            return
        
        response = yield tornado.gen.Task(self.db.pages.remove, {'_id': self.strToObjectId(self.data['_id'])})
        result = self.getMongoResult(response)
        
        self.response(None, 0, True)


class ScreenHandler(CoreHandler):
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        if 'page' not in self.arguments:
            self.response("arguments not found", 10, False)
            return
        
        response = yield tornado.gen.Task(self.db.screen.find, {'page': self.arguments['page']})
        result = self.getMongoResult(response)
        
        self.response([self.objectIdToStr(item) for item in result], 0, True)
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        if 'browsers' and 'pages' and 'resolution' not in self.data:
            self.response("arguments not found", 10, False)
            return
        
        socket_id = self.get_cookie('socket_id')
        if socket_id is None:
            Exception("socket_id is None.")
        
        for k,v in self.data.items():
            if (type(v) is not list):
                self.data[k] = [v]
        
        for pageId in self.data['pages']:
            response = yield tornado.gen.Task(self.db.pages.find_one, {'_id': self.strToObjectId(pageId)})
            page = self.getMongoResult(response)
            if (not page): continue
            
            for browserId in self.data['browsers']:
                system, browser, version = browserId.split('_')
                
                for resolutionId in self.data['resolution']:
                    criteria = {'page': pageId, 'system': system, 'browser': browser, 'version': version, 'resolution': resolutionId}
                    
                    response = yield tornado.gen.Task(self.db.screen.update, criteria, dict(criteria.items() + {'ready': 0, 'images': {}}.items()), True)
                    result = self.getMongoResult(response)
                    
                    response = yield tornado.gen.Task(self.db.screen.find_one, criteria)
                    screen = self.getMongoResult(response)
                    
                    rowId = screen['_id']
                    addTask(self.objectIdToStr(rowId), page['url'], pageId, system, browser, version, resolutionId, socket_id)
        
        self.response({}, 0, True)


class ImageHandler(CoreHandler):
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        if 'screen' and 'type' not in self.arguments:
            self.response("arguments not found", 10, False)
            return
        
        response = yield tornado.gen.Task(self.db.screen.find_one, {'_id': self.strToObjectId(self.arguments['screen'])})
        screen = self.getMongoResult(response)
        
        if screen['ready'] == 0:
            self.redirect('/static/img/wait.jpg')
            self.finish()
            return
        
        fs = gridfs.GridFS(self.db)
        try:
            image = fs.get_version(self.arguments['screen'] + self.arguments['type'])
            self.set_header("Content-Type", 'image/jpeg')
            self.write(image.read())
        except:
            self.redirect('/static/img/not-found.jpg')
        
        self.finish()

class WebSocket(websocket.WebSocketHandler):
    def open(self):
        logging.info("WebSocket opened")
        
    def on_message(self, message):
        socket_id = message
        logging.info("WebSocket message: {0}".format(socket_id))
        
        self.application.webSocketsPool[socket_id] = self

    def on_close(self):
        for key, value in self.application.webSocketsPool.items():
            if value == self:
                del self.application.webSocketsPool[key]
                del self.application.tasksPool[key]
                
        logging.info("WebSocket closed")
        
class UpdateWorkerHandler(CoreHandler):
    def get(self):
        UpdateWorkerTask()

@task
def addTask(rowId, pageUrl, pageId, system, browser, version, resolutionId, socket_id):
    """
    смотрим system (win7, winxp, ubuntu)
    и создаем задачу в нужном потоке
    """
    
    # опции для задачи
    options = [rowId, pageUrl, pageId, browser, resolutionId, socket_id]
    
    # очередь, куда отправлять задачу, будет название OS - system
    asyncResult = send_task("worker.getScreen", options, queue = "%s_%s_%s" % (system, browser,version))
    
    if(socket_id in application.tasksPool):
        application.tasksPool[socket_id].append(asyncResult)
    else:
        application.tasksPool[socket_id] = [asyncResult]
        
@task
def UpdateWorkerTask():
    """
    задача: Обновление worker'а
    """
    send_task("worker.updateWorker", ["Updating Worker!"], queue = "updating")

    
def checkTasksState():
    #logging.info("Start checkTasksState: webSocketsPool count - {0}. tasksPool count - {1}".format(len(application.webSocketsPool),len(application.tasksPool)))
    for socket_id in application.tasksPool:
        for task in application.tasksPool[socket_id]:
            if task.ready():
                logging.info("RESULT SENDING: {0}".format(task.result))
                application.webSocketsPool[socket_id].write_message(task.result)
                application.tasksPool[socket_id].remove(task)

class Application(tornado.web.Application):
    def __init__(self):
        
        # Loading configurations for APP
        configs = ScreenshotConfigs()
        mongo_conf = configs.GiveMongoConnectionConf()

        # MongoDB
        self.db = asyncmongo.Client(pool_id='facerotate_db_connection', host=mongo_conf['host'], port=mongo_conf['port'], dbname=mongo_conf['database'])
        
        self.webSocketsPool= {}
        self.tasksPool= {}

        handlers = [
            (r"/",              MainHandler),
            (r"/site",          SitesHandler),
            (r"/page",          PagesHandler),
            (r"/screen",        ScreenHandler),
            (r"/image",         ImageHandler),
            (r"/static/(.*)",   tornado.web.StaticFileHandler, {"path": os.path.join(APP_DIR, 'static')}),
            (r"/websocket",     WebSocket),
            (r"/updateworker",  UpdateWorkerHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

application = Application()
class TornadoDaemon(Daemon):
    def run(self):
        application.listen(8888)
        IOLoopInstance = tornado.ioloop.IOLoop.instance()
        
        configs = ScreenshotConfigs()
        tornado_settings = configs.GiveTornadoSettings()
        
        # checking tasks'r state for notify users
        periodic = tornado.ioloop.PeriodicCallback(checkTasksState, float(tornado_settings["checktacks_time"]))
        periodic.start()
        
        IOLoopInstance.start()

if __name__ == "__main__":
    
    tornado.options.parse_command_line()
    pid_file = os.path.join(APP_DIR, 'tornado.pid')
    log_file = os.path.join(APP_DIR, '..', 'logs', 'tornado.log')

    daemon = TornadoDaemon(pid_file, stdout=log_file, stderr=log_file)
    daemon.run()
    """
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
    """