# -*- coding: utf-8 -*-
import scrapy

from ..spiders.base import BaseSpider

class FateTomorrowSpider(BaseSpider):
    name = 'fate_year'
    allowed_domains = ['astro.sina.com.cn']
    start_urls = ['http://astro.sina.com.cn/']

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

    def __init__(self, production=False, *args, **kwargs):
        BaseSpider.__init__(self, production, *args, **kwargs)
        self.name = "fate_year"

    def start_requests(self):
        for constell in self.astro_manager.getConstell():
            url = self.astro_manager.next_url(self.start_urls[0], constell, self.name)
            para = {"constell": constell, "fate": self.name}
            yield scrapy.Request(url, callback=self.astro_manager.fate_base, meta={"para": para}, dont_filter=True)




