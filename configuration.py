# -*- coding: utf-8 -*-
import ConfigParser, os.path

class ScreenshotConfigs():
    """
    Provide methods to define configuration of project.
    It uses config file "config.ini". In __init__() we show path to or config file. That is standart INI file with its sections.

    """

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        
        self.config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'))

    def GiveTornadoSettings(self):
        """
        It returns Tornado settings
        """
        tornado = {}
        
        try:
            tornado['checktacks_time'] = self.config.get('Tornado', 'TORNADO_CHECKTASKS_TIME')
            tornado['checkworkers_time'] = self.config.get('Tornado', 'TORNADO_CHECKWORKERS_TIME')
        except ConfigParser.NoOptionError:
            tornado['checktacks_time'] = None

        return tornado

    def GiveMongoConnectionConf(self):
        """
        It returns MongoDB connection configuration
        """
        mongo = {}
        try:
            mongo['port'] = self.config.getint('Mongo', 'MONGODB_PORT')
        except ConfigParser.NoOptionError:
            mongo['port'] = None
        
        try:
            mongo['host'] = self.config.get('Mongo', 'MONGODB_HOST')
        except ConfigParser.NoOptionError:
            mongo['host'] = None

        try:
            mongo['database'] = self.config.get('Mongo', 'MONGODB_DATABASE')
        except ConfigParser.NoOptionError:
            mongo['database'] = None

        return mongo