# -*- coding: utf-8 -*-
import logging
from enumcom import BaseEnum, AstroEnum

class AstroDataManager(object):
    def __init__(self, mysqlInstance):
        self.mysqlInstance = mysqlInstance
        self.source = BaseEnum.DataSourceEnum
        self.constell = AstroEnum.ConstellationEnum
        self.logger = logging.getLogger('AstroDataManager')

    def getConstell(self):
        # 白羊座，金牛座 双子座 巨蟹座 狮子座 处女座 天秤座 天蝎座 射手座 摩羯座 水瓶座 双鱼座
        constellations = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius',
                          'Capricorn', 'Aquarius', 'Pisces']
        return constellations

    def fate_base(self, response):
        data = self.article(response)
        data["source"] = self.source.SINA.value
        para = dict(response.meta["para"])
        fate = para["fate"]
        constell = para["constell"]
        self.fate_detail(data, response, constell, fate)
        self.mysqlInstance.creat_table(fate)
        sql = self.mysqlInstance.create_insert_sql(data, fate)
        self.mysqlInstance.execute_sql(sql, None)

    def next_url(self, url, astroName, dayType):
        next_url = url + dayType + "_" + astroName + "/"
        return next_url

    def article(self, response):

        item = dict()
        article = response.xpath("//div[@class='article_mod']")
        head = article.xpath("./div[@class='head clearfix']")
        item["name"] = head.xpath("./div[@class='tit']/div[@class='tit_n']/text()").extract()[0].strip()
        item["astro_time"] = head.xpath("./div[@class='tit']/div[@class='tit_d']/text()").extract()[0].strip()
        item["valid_time"] = head.xpath("./div[@class='info']/div[@class='time']/text()").extract()[0].strip().split("：")[1]
        return item

    def fate_detail(self, data, response, constell, fate):
        content = response.xpath("//div[@class='article_mod']/div[@class='content clearfix']")
        print(fate)
        if not content:
            logging.info("{}, {} 获取标签错误", fate, constell)
            return
        if fate in ["fate_day", "fate_tomorrow"]:
            return self.day_detail(content, data)
        if fate in ["fate_week", "fate_month"]:
            return self.week_month_detail(content, data)
        if fate in ["fate_year"]:
            return self.year_detail(content, data)
        if fate in ["fate_year_love"]:
            return self.love_detail(content, data)
        return data

    def day_detail(self, content, data):
        trs = content.xpath("./table[@class='tb']/tr")
        for tr in trs:
            tds = tr.xpath("./td")
            for i in range(0, len(tds), 2):
                tag = tds[i].xpath("string(.)").extract()[0].strip()
                label = self.getLabel(tag)
                if label == None or label.strip() == '':
                    continue
                ss = tds[i+1].xpath("string(.)").extract()[0].strip()
                data[label] = ss
        return data

    def week_month_detail(self, content, data):
        divs = content.xpath("./div")
        for i in range(0, len(divs), 2):
            tag = divs[i].xpath("./span")
            if len(tag) <= 0:
                continue
            tag_name = tag[0].xpath("string(.)").extract()[0]
            label = self.getLabel(tag_name)
            if label == None:
                continue
            if len(tag) == 2 and tag[1].xpath("string(.)").extract()[0].strip() != '':
                data[label] = tag[1].xpath("string(.)").extract()[0]
                continue
            if divs[i].xpath("./i"):
                star = label + "_" + divs[i].xpath("./i")[1].xpath("./@class").extract()[0]
                data[star] = len(divs[i].xpath("./i"))
            if ("TIPS" not in tag_name) and ("新尝试" not in tag_name):
                label = label + "_desc"
            data[label] = divs[i + 1].xpath("string(.)").extract()[0].strip()

        return data

    def year_detail(self, content, data):

        divs = content.xpath("./div")
        data["title"] = divs[0].xpath("string(.)").extract()[0]
        data["summary"] = divs[4].xpath("string(.)").extract()[0].strip()
        divs = divs[5:-1]
        for i in range(0, len(divs), 2):
            tag = divs[i].xpath("./span")
            if len(tag) <= 0:
                continue
            tag_name = tag[0].xpath("string(.)").extract()[0]
            if tag_name == '' or tag_name == None:
                continue
            label = self.getLabel(tag_name) + "_desc"
            data[label] = divs[i + 1].xpath("string(.)").extract()[0].strip()
        return data

    def love_detail(self, content, data):
        divs = content.xpath("./div")
        summary_ps = divs[0].xpath("./p")[1:]

        data["summary"] = "".join(summary_ps.xpath("string(.)").extract()).strip()
        data["girl"] = divs[2].xpath("string(.)").extract()[0].strip()
        data["boy"] = divs[4].xpath("string(.)").extract()[0].strip()
        return data

    def getLabel(self, tag):
        labelItem = {"幸运值": "luck", "爱情指数": "love_index", "工作指数": "work_index", "财运指数": "fortune_index",
                 "健康指数": "health_index", "幸运数字": "lucky_num", "幸运颜色": "lucky_color", "贵人星座": "noble_constellation",
                 "重要天象": "important", "精评": "fine_review", "详述": "dilatino", "整体运势": "entirety", "爱情运": "love",
                 "工作学业": "work_study", "工作理财": "work_finance", "工作": "work", "事业": "work", "财运": "finance", "健康": "health",
                 "本月": "tips", "新尝试": "new_attempt", "开运方位": "lucky_location", "高照日": "lucky_day", "警报日": "alert_day",
                 "社交贵人": "gam_noble"}

        for key in labelItem.keys():
            if key not in tag:
                continue
            else:
                return labelItem[key]
        return None

    def merge(self, targetDict, srcDict):
        res = {**targetDict, **srcDict}
        return res
