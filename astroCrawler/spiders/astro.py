# -*- coding: utf-8 -*-
import scrapy

from component.mysql_connect import MySQLInstance
from ..spiders.base import BaseSpider
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
    constellations = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    fate_types = ['fate_day', 'fate_tomorrow', 'fate_week', 'fate_month', 'fate_year', 'fate_year_love']

    def __init__(self, production=False, *args, **kwargs):
        BaseSpider.__init__(self, production, *args, **kwargs)



    def start_requests(self):
        for fate in self.fate_types:
            for constell in self.constellations:
                url = BaseSpider.next_url(constell, fate)
                yield scrapy.Request(url, callback=self.fate_day, dont_filter=True)

    def fate_day(self, response):
        article = response.xpath("//div[@class='article_mod']")
        head =  article.xpath("./div[@class='head clearfix']")
        titName = head.xpath("./div[@class='tit']/div[@class='tit_n']").extract()[0].strip()
        titDate = head.xpath("./div[@class='tit']/div[@class='tit_d']").extract()[0].strip()
        fateType = head.xpath("./div[@class='info']/div[@class='info_m']/span[class='sp1']").extract()[0].strip()
        validTime = head.xpath("./div[@class='info']/div[@class='time']]").extract()[0].strip()

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


