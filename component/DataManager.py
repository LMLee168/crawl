# -*- coding: utf-8 -*-
import logging

class SeedDataManager(object):
    def __init__(self, mysqlInstance):
        self.mysqlInstance = mysqlInstance
        self.logger = logging.getLogger('DataManager')

    def insert(self):
        pass