# -*- coding: utf-8 -*-
import scrapy

from ..spiders.base import BaseSpider
from astroCrawler.items import StarcrawlerItem
import time
import datetime

class StarSpider(BaseSpider):
    name = 'star'
    allowed_domains = ['star.iecity.com']
    start_urls = ['http://star.iecity.com']

    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    output_file = today + ".txt"

    def __init__(self, production=False, *args, **kwargs):
        BaseSpider.__init__(self, production, *args, **kwargs)
        self.name = "star"

    def start_requests(self):
        url = "http://star.iecity.com/all"
        req = scrapy.Request(url, callback=self.parse_info)
        yield req

    def parse_info(self, response):
        subjects = response.xpath("//ul[@class='starlist1 clearfix']/li")
        items = []
        for subject in subjects:
            item = StarcrawlerItem().initField()
            star_url = self.start_urls[0] + subject.xpath("./a/@href").extract()[0]
            star_name = subject.xpath("./a/img/@alt").extract()[0]
            star_photo_url = subject.xpath("./a/img/@data-original").extract()[0]

            item['name'] = star_name
            item['avatar'] = star_photo_url
            item['source'] = self.source.DataSourceEnum.SINA.value
            yield scrapy.Request(star_url, callback=self.parse_data, meta={'item': item})
        # self.write_to_db(items, "star")
        next_url = self.start_urls[0] + response.xpath("//div[@class='Pager']/span[12]/a/@href").extract()[0]
        yield scrapy.Request(next_url, callback=self.parse_info, dont_filter=True)

    def parse_data(self, response):

        item = response.meta['item']
        data_tr = response.xpath("//table[@class='Detail table5']/tr")
        gender = data_tr.xpath("./td[@itemprop='gender']/text()").extract()[0].strip()
        nationality = data_tr.xpath("./td[@itemprop='nationality']/text()").extract()[0].strip()
        item['gender'] = self.gender.GenderEnum.MALE.num if self.gender.GenderEnum.MALE.chinese == gender else self.gender.GenderEnum.FEMALE.num
        item['nationality'] = nationality
        birth = data_tr.xpath("./td[@itemprop='birthDate']/text()").extract()
        item['birthday'] = birth[0].strip() if birth else ""
        data_content = response.xpath("string(//div[@class='border content']/div[2]/div[@itemprop='description'])")
        item['introduction'] = data_content.extract()[0].strip()

        # item['native_place'] = ""
        # item['constellation'] = ""
        # item["hobby"] = ""
        # item['job'] = ""
        # item['height'] = ""
        # item['weight'] = ""
        data_ps = response.xpath("//div[@class='border content']/div[2]/p")
        for p in data_ps:
            tag = p.xpath("./strong/text()").extract()[0].rstrip("：").strip()
            label = self.getLabel(tag)
            if label == None:
                continue
            item[label] = p.xpath("./text()").extract()[0].strip("cm").strip("kg")
            # if "籍贯" in tag:
            #     item['native_place'] = p.xpath("./text()").extract()[0].strip()
            # if "星座" in tag:
            #     item['constellation'] = p.xpath("./text()").extract()[0].strip()
            # if "爱好" in tag:
            #     item["hobby"] = p.xpath("./text()").extract()[0].strip()
            # if "职业" in tag:
            #     item['job'] = p.xpath("./text()").extract()[0].strip()
            # if "身高" in tag:
            #     item['height'] = p.xpath("./text()").extract()[0].strip("cm")
            # if "体重" in tag:
            #     item['weight'] = p.xpath("./text()").extract()[0].strip("kg")

        item["photos"] = self.parse_photos(response)

        item["createTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["updateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.write_to_db(dict(item), "star")
        # return  item

    def parse_photos(self, content):
        photo_contents = content.xpath("//div[@class='flex-images']/div[@class='item']")
        photos = []
        num = 0
        for i in range(len(photo_contents)):
            photo = photo_contents[i].xpath("./a/@href").extract()[0].strip()
            photos.append(photo)
            num  = num + 1
            if num == 3:
                break
        return photos

    def write_to_db(self, item, info_key):
        if info_key == "star":
            self.instance.creat_table(info_key)
            sql = self.instance.create_insert_sql(item, info_key)
            self.instance.execute_sql(sql, None)

    def write_to_txt(self, item, info_key):
        output_file = ""
        if info_key == "star":
            output_file = info_key + "_" + self.output_file
        with open(output_file, "a") as f:
            f.write(str(item) + "\n")
            # f.write(json.dumps(item, cls= self.change_type(),indent=4 ,ensure_ascii=False))

    def getLabel(self, tag):
        labelItem = {"籍贯": 'native_place', "星座": 'constellation', "爱好": "hobby", "职业": 'job', "身高": 'height', "体重": 'weight'}
        for key in labelItem.keys():
            if key not in tag:
                continue
            else:
                return labelItem[key]
        return None

    #增量爬取（网页信息变更/出现新页面）---对Request对象生成指纹
    # def request_fingerprint(self, include_headers = None):
    #     if include_headers:
    #         include_headers = tuple(to_bytes(h.lower())) for h in sorted(include_headers))