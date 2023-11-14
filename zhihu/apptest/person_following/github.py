import re
import subprocess
import hashlib
import requests
import json
from tqdm import tqdm
import time


# coding=utf-8
import hashlib
import execjs
import base64
import os
import time
import random
import csv
import json
import re

REG = re.compile('<[^>]*>')
session = requests.Session()

with open('X_zse_96.js', 'r', encoding='utf-8') as f:
    jstext = f.read()
ctx_96 = execjs.compile(jstext)


def get_x_zse_96(ta,api, cookie_dc_2):
    tt_codes = ta +'+'+api+'+'+ cookie_dc_2
    print(tt_codes)
    hl = hashlib.md5()
    hl.update(tt_codes.encode('utf-8'))
    res_md5 = hl.hexdigest()
    print(res_md5)
    result = ctx_96.call('func', res_md5)
    return result


url_token = '72-31-98-7'


def user_followees(page_N):
    offset = (page_N-1) * 20
    ta = "101_3_3.0"
    cookie_dc0 = "\"APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843\""
    uh = "/api/v4/members/"+url_token + \
        "/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=" + \
        str(offset)+"&limit=20"

    x_961 = get_x_zse_96(ta,uh,cookie_dc0)

    tf = ta+'+'+uh+'+'+cookie_dc0
    print(tf)
    md5 = hashlib.md5()
    md5.update(tf.encode('utf-8'))
    tt = md5.hexdigest()
    print(tt)
    x_96 = ctx_96.call("func", tt)
    print(x_961==x_96)

    url = "https://www.zhihu.com/api/v4/members/"+url_token + \
        "/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=" + \
        str(offset)+"&limit=20"

    headers = {
        'accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        #    'Accept-Encoding':'gzip, deflate, br',
        'X-Requested-With': 'fetch',
        'Referer': 'https://www.zhihu.com/people/'+url_token+'/followees?page='+str(page_N),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        "cookie": 'd_c0="APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843"; _xsrf=HWUgSh20t0DqcQLELvW9aiBDUF9b33tF; q_c1=6b8c51f29aec40b3b5de4a5680882bf3|1645958464000|1645958464000; _zap=b0db2c52-aac3-45a9-a4b5-63fc4e67e0a7; z_c0=2|1:0|10:1697629107|4:z_c0|80:MS4xTF91WkNBQUFBQUFtQUFBQVlBSlZUYXVVRjJZaWVpSXRndFd6RWdCUmwyY2VPdUh1M0djcnZRPT0=|3d38eb60e492abff77f7753d24cb396b164247ad6275aead6368921d317f57af; tst=r; SESSIONID=nBWT56da7Tfbt9dMoNPWtyCxaWHtbdSNAKJ9HiQFaPI; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1698741524|1698739803',
        "x-zse-93": "101_3_3.0",
        'x-zse-96': x_96
    }
    responses = requests.get(url=url, headers=headers)
    resp_code = responses.status_code
    if resp_code == 200:
        print('状态码'+str(resp_code))
    # print(responses.json()["paging"]["next"])

if __name__ == "__main__":
    for i in range(0, 2):
        user_followees(i)
