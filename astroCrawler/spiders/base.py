# -*- coding: utf-8 -*-
import scrapy
from component.mysql_connect import MySQLInstance
from component.AstroDataManager import AstroDataManager
from enumcom import BaseEnum

class BaseSpider(scrapy.Spider):

    def __init__(self, production=False, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.logger.info('login database production is %s, type: %s' % (production, type(production)))
        # if production is True or production == 'True':
        host = '10.3.250.22',
        user = 'developer',
        password = '!1qaz2wsx3EDC',
        database = 'astro',
        port = 3306,
        use_unicode = 'utf8',
        # else:
        user = 'root'
        host = '127.0.0.1'
        database = 'astro'
        password = '111111'
        # user = 'developer'
        # host = '10.3.250.22'
        # database = 'astro'
        # password = '!1qaz2wsx3EDC'
        self.instance = MySQLInstance.create_instance(user, password, host, database)
        self.astro_manager = AstroDataManager(self.instance)
        self.source = BaseEnum.DataSourceEnum
        self.gender = BaseEnum.GenderEnum

