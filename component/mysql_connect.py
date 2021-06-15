#!/usr/bin/python
# -*-coding:utf-8-*-
import re
import mysql.connector
from mysql.connector import errorcode
import logging

class MySQLInstance(object):

    @classmethod
    def __init__(self, user, passwd, host, database):
        self.conn = mysql.connector.connect(user=user,
                                            password=passwd,
                                            host=host,
                                            database=database)
        pass

    @classmethod
    def create_instance(cls, user, passwd, host, database):
        try:
            inst = cls(user, passwd, host, database)
            return inst
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            exit(-1)

    @classmethod
    def table_exists(self,  table_name):
        sql = "show tables;"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1  # 存在返回1
        else:
            return 0


    @classmethod
    def create_insert_sql(self, item, info_key):
        insert_sql = "insert into " + info_key  + "({}) values ({})"
        keys, values = self._create_insert_sql(item)
        insert = insert_sql.format(keys, values)
        return insert

    @classmethod
    def _create_insert_sql(self, star_info):
        keys, values = [], []
        for key, value in star_info.items():
            if value != '' and value is not None and value != 'None':
                keys.append(key)
                values.append(value)
        return ','.join(keys), \
               ','.join(["'" + str(v).replace("'", "\\'").replace('&#39;', "\\'") + "'" for v in values])

    @classmethod
    def creat_table(self,  item, info_key):
        code  = self.table_exists( info_key)
        if ( code != 1 ):
            print("table with info_key is not exists !")
            match_sql = self.create_star_table_sql(info_key)
            self.execute_sql(match_sql)

    @classmethod
    def execute_sql(self, sql, values=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, values)
        self.conn.commit()
        result = cursor.rowcount
        cursor.close()
        return result

    def batch_execute_sql(self, sql, values=None):
        cursor = self.conn.cursor()
        cursor.executemany(sql, values)
        self.conn.commit()
        result = cursor.rowcount
        cursor.close()
        return result

    @classmethod
    def create_star_table_sql(self, info_key):
        if info_key == "star" :
            return '''
                    CREATE TABLE star (
                      id bigint(20) primary key NOT NULL AUTO_INCREMENT,
                      name varchar(10) NOT NULL comment "名字",
                      avatar varchar(150) default NULL comment "头像",
                      gender varchar(20) default NULL comment "性别",
                      nationality varchar(20) default NULL comment "国籍",
                      native_place varchar(50) default NULL comment "籍贯",
                      birthday datetime default NULL comment "生日",
                      job varchar(50) default NULL comment "职业",
                      height int(4) default  null comment "身高",
                      weight int(4) default  null comment "体重",
                      constellation varchar(50) default  null comment "星座",
                      hobby varchar(200) default  null comment "爱好",
                      introduction text default  null comment "介绍",
                      photos varchar(500) default  null comment "相册",
                      createTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                      updateTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                      UNIQUE KEY index_id (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='明星信息表'
                '''
        if info_key == "fate_day":
            return '''
                    CREATE TABLE fate_day (
                       id bigint(20) primary key NOT NULL AUTO_INCREMENT,
                       name varchar(10) NOT NULL comment "星座名称",
                       astro_time varchar(50) default NULL comment "星座时间",
                       valid_time varchar(50) default NULL comment "有效日期",
                       luck varchar(10) default  null comment "幸运值",
                       love_index varchar(10) default  null comment "爱情指数",
                       work_index varchar(10) default  null comment "工作指数",
                       fortune_index varchar(10) default  null comment "财运指数",
                       health_index varchar(10) default  null comment "健康指数",
                       lucky_num varchar(10) default  null comment "幸运数字",
                       lucky_color varchar(10) default  null comment "幸运颜色",
                       noble_constellation varchar(10) default  null comment "贵人星座",
                       important_ varchar(500) default  null comment "重要天象",
                       fine_review varchar(500) default  null comment "精评",
                       dilatino varchar(500) default  null comment "详述",
                        createTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updateTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        UNIQUE KEY index_id (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='今日运势表'
                '''

        if info_key == "fate_tomorrow":
            return '''
                    CREATE TABLE fate_tomorrow (
                      id bigint(20) primary key NOT NULL AUTO_INCREMENT,
                       name varchar(10) NOT NULL comment "星座名称",
                       astro_time varchar(50) default NULL comment "星座时间",
                       valid_time varchar(50) default NULL comment "有效日期",
                       luck varchar(10) default  null comment "幸运值",
                       love_index varchar(10) default  null comment "爱情指数",
                       work_index varchar(10) default  null comment "工作指数",
                       fortune_index varchar(10) default  null comment "财运指数",
                       health_index varchar(10) default  null comment "健康指数",
                       lucky_num varchar(10) default  null comment "幸运数字",
                       lucky_color varchar(10) default  null comment "幸运颜色",
                       noble_constellation varchar(10) default  null comment "贵人星座",
                       important_ varchar(500) default  null comment "重要天象",
                       fine_review varchar(500) default  null comment "精评",
                       dilatino varchar(500) default  null comment "详述",
                        createTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updateTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        UNIQUE KEY index_id (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='明日运势表'
                '''

        if info_key == "fate_week":
            return '''
                    CREATE TABLE fate_week (
                      id bigint(20) primary key NOT NULL AUTO_INCREMENT,
                       name varchar(10) NOT NULL comment "星座名称",
                       astro_time varchar(50) default NULL comment "星座时间",
                       valid_time varchar(50) default NULL comment "有效日期",
                       entirety varchar (20) default NULL comment "整体运势",
                       entirety_star int(4) default NULL comment "星级 满5星",
                       entirety_desc text default null comment "整体运势描述"
                        love varchar (20) default NULL comment "爱情运势",
                        love_star int(4) default NULL comment "星级 满5星",
                        love_desc text default null comment "爱情运势描述"
                        work_study varchar (20) default NULL comment "工作学业运势",
                        work_study_star int(4) default NULL comment "星级 满5星",
                        work_study_desc text default null comment "工作学业运势描述"
                       noble_constellation varchar(10) default  null comment "贵人星座",
                       new_attempt varchar(500) default  null comment "新尝试",
                       location varchar(20) default  null comment "开运方位/地点",
                       lucky_star_day varchar(20) default  null comment "吉星高照日",
                       red_alert_day varchar(20) default  null comment "红色警报日", 
                      createTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                      updateTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                      UNIQUE KEY index_id (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='周运势表'
                '''

        if info_key == "fate_month":
            return '''
                    CREATE TABLE fate_month (
                      id bigint(20) primary key NOT NULL AUTO_INCREMENT,
                       name varchar(10) NOT NULL comment "星座名称",
                       astro_time varchar(50) default NULL comment "星座时间",
                       valid_time varchar(50) default NULL comment "有效日期",
                       tips text default  null comment "本月tips",
                       entirety varchar (20) default NULL comment "整体运势",
                       entirety_star int(4) default NULL comment "星级 满5星",
                       entirety_desc text default null comment "整体运势描述"
                        love varchar (20) default NULL comment "爱情运势",
                        love_star int(4) default NULL comment "星级 满5星",
                        love_desc text default null comment "爱情运势描述",
                        work_finance varchar (20) default NULL comment "工作理财运势",
                        work_finance_star int(4) default NULL comment "星级 满5星",
                        work_finance_desc text default null comment "工作理财运势描述"
                      createTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                      updateTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                      UNIQUE KEY index_id (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='月运势表'
                '''

        if info_key == "fate_year":
            return '''
                    CREATE TABLE fate_year (
                      id bigint(20) primary key NOT NULL AUTO_INCREMENT,
                       name varchar(10) NOT NULL comment "星座名称",
                       astro_time varchar(50) default NULL comment "星座时间",
                       valid_time varchar(50) default NULL comment "有效日期",
                       title varchar(500) default null comment "标题",
                       summary text default null comment "综述",
                        love varchar(500) default null comment "爱情运标题",
                        love_desc text default null comment "爱情运描述",
                        work varchar(500) default null comment "工作运标题",
                        work_desc text default null comment "工作运描述",
                        gam_noble varchar(500) default null comment "社交贵人运标题",
                        gam_noble_desc text default null comment "社交贵人运描述",
                        health varchar(500) default null comment "健康运标题",
                        health_desc text default null comment "健康运描述",
                        wealth varchar(500) default null comment "财运标题",
                        wealth_desc text default null comment "财运描述",
                      createTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                      updateTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                      UNIQUE KEY index_id (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='年运势表'
                '''

        if info_key == "fate_year_love":
            return '''
                    CREATE TABLE fate_year_love (
                      id bigint(20) primary key NOT NULL AUTO_INCREMENT,
                       name varchar(10) NOT NULL comment "星座名称",
                       astro_time varchar(50) default NULL comment "星座时间",
                       valid_time varchar(50) default NULL comment "有效日期",
                       desc text default  null comment "描述",
                       girl_desc text default null comment "女生描述",
                       boy_desc text default  null comment "男生描述",
                      createTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                      updateTime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                      UNIQUE KEY index_id (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='年度爱情运势表'
                '''
