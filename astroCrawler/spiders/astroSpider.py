# -*- coding: utf-8 -*-
import scrapy

from component.DBsql import DB
from ..items import AstrocrawlerItem
import time
import json
import datetime

class AstroSpider(scrapy.Spider):
    name = 'astro'
    allowed_domains = ['astro.sina.com.cn']
    start_urls = ['http://astro.sina.com.cn']

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'soda_spider.spiders.base_spider.UploadImageWithPipeline': 300,
            # 'soda_spider.spiders.base_spider.SaveInfoPipeline': 301,
            # 'soda_spider.spiders.base_spider.MyImagesPipeline': 260,
        },
        # 'COOKIES_DEBUG': True,
        # 'LOG_FILE': '/data/logs/movie_scrapy.{}-{}.log'.format(today.date(), int(time.time())),
        'LOG_LEVEL': 'DEBUG',
        'AUTOTHROTTLE_ENABLED': True,
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 5,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
        'HTTPERROR_ALLOW_ALL': True
    }
    #白羊座，金牛座 双子座 巨蟹座 狮子座 处女座 天秤座 天蝎座 射手座 摩羯座 水瓶座 双鱼座
    constellation = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    fate_type = ['fate_day', 'fate_tomorrow', 'fate_week', 'fate_month', 'fate_year', 'fate_year_love']


    def start_requests(self):
        pass

    def fate_day(self, response):
        pass

    def fate_tomorrow(self, response):
        pass

    def fate_week(self, response):
        pass

    def fate_month(self, response):
        pass

    def fate_year(self, response):
        pass

    def fate_year_love(self, response):
        pass


