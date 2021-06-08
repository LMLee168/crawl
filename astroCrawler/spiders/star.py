# -*- coding: utf-8 -*-
import scrapy

from component.DBsql import DB
from ..items import StarcrawlerItem
import time
import json
import datetime

class StarSpider(scrapy.Spider):
    name = 'star'
    allowed_domains = ['star.iecity.com']
    start_urls = ['http://star.iecity.com']

    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    output_file = today + ".txt"

    def start_requests(self):
        url = "http://star.iecity.com/all"
        req = scrapy.Request(url, callback=self.parse_info)
        yield req

    def parse_info(self, response):
        subjects = response.xpath("//ul[@class='starlist1 clearfix']/li")
        items = []
        for subject in subjects:
            item = {}
            star_url =  self.start_urls[0] + subject.xpath("./a/@href").extract()[0]
            star_name = subject.xpath("./a/img/@alt").extract()[0]
            star_photo_url = subject.xpath("./a/img/@data-original").extract()[0]

            item['name'] = star_name
            item['photo_url'] = star_photo_url
            print(star_url)
            yield scrapy.Request(star_url, callback=self.parse_data, meta={'item': item})

        # self.write_to_db(items, "star")
        next_url = self.start_urls[0] + response.xpath("//div[@class='Pager']/span[12]/a/@href").extract()[0]
        yield scrapy.Request(next_url, callback=self.parse_info, dont_filter=True)

    def parse_data(self, response):

        item = response.meta['item']
        data_tr = response.xpath("//table[@class='Detail table5']/tr")
        gender = data_tr.xpath("./td[@itemprop='gender']/text()").extract()[0].strip()
        nationality = data_tr.xpath("./td[@itemprop='nationality']/text()").extract()[0].strip()
        item['gender'] = gender
        item['nationality'] = nationality
        item['birthday'] = ""
        item['native_place'] = ""
        item['constellation'] = ""
        birth = data_tr.xpath("./td[@itemprop='birthDate']/text()").extract()
        if birth:
            item['birthday'] = birth[0].strip()
        data_ps = response.xpath("//div[@class='border content']/div/p")
        for p in data_ps:
            tag = p.xpath("./strong/text()").extract()[0].rstrip("：").strip()
            if "籍贯" in tag:
                item['native_place'] = p.xpath("./text()").extract()[0].strip()
            if "星座" in tag:
                item['constellation'] = p.xpath("./text()").extract()[0].strip()
        item["createTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["updateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["hobby"] = ""

        self.write_to_txt(item, "star")

    def parse_photos(self, response):
        photos = []

    def write_to_db(self,item,info_key):
        db = DB()
        conn = db.connectdb()
        cursor = conn.cursor()
        if info_key == "star":
            db.insert_matchOne(cursor, item, info_key, conn)

    def write_to_txt(self,item,info_key):
        output_file = ""
        if info_key == "star":
            output_file = info_key + "_" + self.output_file
        with open(output_file,"a") as f:
            f.write(str(item) + "\n")
            # f.write(json.dumps(item, cls= self.change_type(),indent=4 ,ensure_ascii=False))

    #增量爬取（网页信息变更/出现新页面）---对Request对象生成指纹
    # def request_fingerprint(self, include_headers = None):
    #     if include_headers:
    #         include_headers = tuple(to_bytes(h.lower())) for h in sorted(include_headers))