#!/usr/bin/python
# -*-coding:utf-8-*-
import pymysql
import re

class DB(object):

    def connectdb(self):
        conn = pymysql.connect(
            host="10.3.250.22",
            user="developer",
            passwd="!1qaz2wsx3EDC",
            port=3306,
            db = "chengjia",
            use_unicode = 'utf8',
            )
        return conn

    def table_exists(self, cursor, table_name):
        sql = "show tables;"
        cursor.execute(sql)
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1  # 存在返回1
        else:
            return 0

    def insert_matchOne(self, cursor, item, info_key, conn):
        code  = self.table_exists(cursor, info_key)
        if ( code != 1 ):
            print("table with info_key is not exists !")
            match_sql = self.create_table_sql(info_key)
            cursor.execute(match_sql)
        sql = "insert into " + info_key  + "(name,avatar,gender,nationality,native_place,birthday,occupation,height," \
                                           "weight,constellation,hobby,introduction,photos, createTime,updateTime)  " \
                                           "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        val = (item["name"], item['avatar'], item['gender'], item['nationality'], item['native_place'], item['birthday'],
               item['occupation'], item['height'], item['weight'], item['constellation'], item['hobby'], item['introduction'],
               item['photos'], item['createTime'], item['updateTime'])
        try:
            n = cursor.execute(sql, val)
            print(n)
            print(val)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("add error : ", e)
        cursor.close()
        conn.close()

    def create_table_sql(self, info_key):
        if info_key == "star" :
            return '''
                    CREATE TABLE star (
                      id bigint(20) primary key NOT NULL AUTO_INCREMENT,
                      name varchar(10) NOT NULL,
                      avatar varchar(150) default NULL,
                      gender varchar(20) default NULL,
                      nationality varchar(20) default NULL,
                      native_place varchar(50) default NULL,
                      birthday datetime default NULL,
                      occupation varchar(50) default NULL,
                      height int(4) default  null,
                      weight int(4) default  null,
                      constellation varchar(50) default  null,
                      hobby varchar(50) default  null,
                      introduction varchar(500) default  null,
                      photos varchar(500) default  null,
                      createTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                      updateTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                      UNIQUE KEY index_id (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
                '''
