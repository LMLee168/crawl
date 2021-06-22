class AstroBaseParser(object):

    def getConstell(self):
        # 白羊座，金牛座 双子座 巨蟹座 狮子座 处女座 天秤座 天蝎座 射手座 摩羯座 水瓶座 双鱼座
        constellations = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius',
                          'Capricorn', 'Aquarius', 'Pisces']
        return constellations

    def fate_detail(self, response):
        data = self.astro_manager.article(response)
        data["source"] = self.source.DataSourceEnum.SINA.value
        para = dict(response.meta["para"])
        fate = para["fate"]
        constell = para["constell"]
        self.astro_manager.fate_detail(data, response, constell, fate)
        self.instance.creat_table(fate)
        sql = self.instance.create_insert_sql(data, fate)
        self.instance.execute_sql(sql, None)

    def next_url(self, url, astroName, dayType):
        next_url = url + dayType + "_" + astroName + "/"
        return next_url