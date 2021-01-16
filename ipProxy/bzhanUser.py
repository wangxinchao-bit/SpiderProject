# -*- encoding = utf-8 -*-
import random
import os
import shutil
import requests
from lxml import etree
import multiprocessing
import requests
import time
import logging
import sys
import sqlite3
import json
import re
"""
使用之前需要开启代理
"""


class bzhanSpider(object):
    def __init__(self):
        self.queue = multiprocessing.Manager().Queue()
        self.cookie = {
            'domain': '/',
            'expires': 'false',
            'httpOnly': 'false',
            'name': 'buvid3',
            'path': 'Fri, 29 Jan 2021 08:50:10 GMT',
            'value': '7A29BBDE-VA94D-4F66-QC63-D9CB8568D84331045infoc,bilibili.com'
        }
        self.uas = 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; FDR-A01w Build/HuaweiMediaPad) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'

    def producer(self):
        for i in range(1, 10000):
            url = "https://m.bilibili.com/space/" + str(i)
            self.queue.put(url)


    def consumer(self):
        while not self.queue.empty():
            time.sleep(random.randrange(0,4))
            url  = self.queue.get()
            proxy = requests.get("http://127.0.0.1:5010/get/").json()["proxy"]
            proxies = {"http": "http://{}".format(proxy)}

            head = {'User-Agent': self.uas,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'http://space.bilibili.com',
                    'Host': 'm.bilibili.com',
                    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Referer': url}
            mid = url.replace('https://m.bilibili.com/space/', '')
            try:
                html = requests.get(url, headers=head, cookies=self.cookie,proxies=proxies, timeout=10).text
                formats = re.findall(r"window.__INITIAL_STATE__=(.*?);\(function\(\)", html)
                try:
                    data = json.loads(formats[0])["space"]
                    name = data["info"]['name']
                    sex = data["info"]['sex']
                    face = data["info"]['face']
                    level = data['info']['level']
                except:
                    pass
                head = {'User-Agent': self.uas,
                        'X-Requested-With': 'XMLHttpRequest',
                        'Origin': 'http://space.bilibili.com',
                        'Host': 'api.bilibili.com',
                        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Referer': url}
                res = requests.get('https://api.bilibili.com/x/relation/stat?jsonp=jsonp&vmid=' + str(mid),
                                   headers=head, cookies=self.cookie, timeout=10).text
                res_js = json.loads(res)
                following = res_js['data']['following']
                follower = res_js['data']['follower']
                print( mid, name, sex, following, follower, level, face)

            except Exception as e:
                logging.error('error in run function: ' + str(e))
                return

    def main(self):
        self.producer()

        pool = multiprocessing.Pool(10)

        for index in range(1000):
            pool.apply_async(self.consumer)
        pool.close()
        pool.join()

if __name__ == '__main__':
    # please attentiom to the url form of novel form shuquge website
    Siper=bzhanSpider()
    Siper.main()

