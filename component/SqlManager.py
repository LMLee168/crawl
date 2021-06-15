# -*- coding: utf-8 -*-
import logging

class StarManager(object):

    @classmethod
    def insert_star_sql(self, item, info_key):
        sql = "insert into " + info_key + "(name,avatar,gender,nationality,native_place,birthday,job,height," \
                                          "weight,constellation,hobby,introduction,photos, createTime,updateTime)  " \
                                          "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        val = (item["name"], item['avatar'], item['gender'], item['nationality'], item['native_place'], item['birthday'],
        item['job'], item['height'], item['weight'], item['constellation'], item['hobby'], item['introduction'],
        item['photos'], item['createTime'], item['updateTime'])
        sql.format(val)
        logging.info(sql)
        return sql


class FateManager(object):
    def fate(self, item, info_key):
        sql =""




