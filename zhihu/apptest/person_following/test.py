# coding=utf-8
from loguru import logger
import hashlib
import execjs
import base64
import os
import time
import random
import csv
import requests
import json
import re

REG = re.compile('<[^>]*>')

session = requests.Session()
# 获取81参数信息
# 获取96参数信息
with open('X_zse_96.js', 'r', encoding='utf-8') as f:
    jstext = f.read()
ctx_96 = execjs.compile(jstext)


def get_x_zse_96(api, cookie_dc_2):
    hl = hashlib.md5()
    tt_codes = '101_3_3.0'+"+"+api+"+"+cookie_dc_2
    hl.update(tt_codes.encode(encoding='utf-8'))
    res_md5 = hl.hexdigest()
    result = ctx_96.call('func', res_md5)
    return result


url_token = "todo-31-69"


class ZhihuSpider(object):
    def __init__(self, d_c0) -> None:
        self.d_c0 = d_c0

    def get_page(self, pageSize):
        offset = (pageSize-1)*20

        uh = "/api/v4/members/"+url_token + \
            "/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=" + \
            str(offset)+"&limit=20"

        x_zse_96 = get_x_zse_96(uh, self.d_c0)

        url = "https://www.zhihu.com/api/v4/members/"+url_token + \
            "/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=" + \
            str(offset)+"&limit=20"
        
        headers = {
            'accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            #    'Accept-Encoding':'gzip, deflate, br',
            'X-Requested-With': 'fetch',
            'Referer': 'https://www.zhihu.com/people/'+url_token+'/followees?page='+str(pageSize),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            "cookie": 'd_c0="APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843"; _xsrf=HWUgSh20t0DqcQLELvW9aiBDUF9b33tF; q_c1=6b8c51f29aec40b3b5de4a5680882bf3|1645958464000|1645958464000; _zap=b0db2c52-aac3-45a9-a4b5-63fc4e67e0a7; z_c0=2|1:0|10:1697629107|4:z_c0|80:MS4xTF91WkNBQUFBQUFtQUFBQVlBSlZUYXVVRjJZaWVpSXRndFd6RWdCUmwyY2VPdUh1M0djcnZRPT0=|3d38eb60e492abff77f7753d24cb396b164247ad6275aead6368921d317f57af; tst=r; SESSIONID=nBWT56da7Tfbt9dMoNPWtyCxaWHtbdSNAKJ9HiQFaPI; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1698741524|1698739803',
            "x-zse-93": "101_3_3.0",
            'x-zse-96': x_zse_96
        }
        responses = requests.get(url=url, headers=headers)
        print(responses.json())


if __name__ == "__main__":

    cookie_dc0 = "\"APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843\""
    spider = ZhihuSpider(cookie_dc0)
    for pageSize in [1, 2]:
        spider.get_page(pageSize)
