# -*- coding: utf-8 -*-
import base64

import requests
import random

class ProxySettings:
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H3063V134966CP9D"
    proxyPass = "1FA2C2D0F7C07890"
    def __init__(self):

        self.proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }

    def get_proxy(self):
        proxies = {
            "http": self.proxyMeta,
            "https": self.proxyMeta,
        }
        return proxies
    pass

# 配置全局变量
# 数据管理
# dataManager = DataManager()
# 文件上传
# ossUploader = OssUploader('soda-cover')
# 电影管理
# movieManager = MovieManager(dataManager, ossUploader)

global_proxy = ProxySettings()
