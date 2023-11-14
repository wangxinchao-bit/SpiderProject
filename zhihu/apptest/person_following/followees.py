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
with open('X_zse_96.js', 'r', encoding='utf-8') as f:
    jstext = f.read()
ctx_96 = execjs.compile(jstext)


def get_x_zse_96(api, cookie_dc_2, js_81):
    hl = hashlib.md5()
    tt_codes = '101_3_3.0'+"+"+api+"+"+cookie_dc_2 + "+"+js_81
    hl.update(tt_codes.encode(encoding='utf-8'))
    res_md5 = hl.hexdigest()
    result = ctx_96.call('func', res_md5)
    return result


def extract_answer(self, s):
    temp_list = REG.sub("", s).replace("\n", "").replace(" ", "")
    return temp_list


class ZhihuSpider(object):
    def __init__(self,d_c0,kession) -> None:
        self.d_c0 =d_c0
        self.kession = kession 

    def get_page(self,offset):
 
        target_url = f'https://www.zhihu.com/api/v4/members/72-31-98-7/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset={offset}&limit=20'
        api = target_url.replace("https://www.zhihu.com", "")
        with open('X_Zst81.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
            js_text = execjs.compile(js_code)
            js_81 = js_text.call('x_81')
        x_zse_96 = get_x_zse_96(api, self.d_c0, js_81)

        my_header = {
            # 'Cookie': "d_c0=AJDRlpCWcBePTplxv4LEeOvuXHDFb7A7W-k=|1695472653;",
            'Cookie': f"_zap=7fee7e89-4821-4883-bcaf-79bcd51f3c9f; d_c0=AICTUe2WlBePTrFSaV0AlIhdFAJwtto1Kr4=|1697888667; captcha_session_v2=2|1:0|10:1697888667|18:captcha_session_v2|88:Q1FFWXRJaC9zK243ZFVXQ2l3WG5YcnNzUDhSSjBqWFNQZkJSRWxIL1pWVzQ2T2NVM0p0dTBKc3lwVDRjSzJxNA==|5c87616dfa48b74d88d45be662bf68b09a3d8d3f01181bca72dcb88fab77fcd6; __snaker__id=4QivuMV5XBVKoUFa; gdxidpyhxdE=Ah9Awy0%5CrE%2B%2BtUVjBdzw8dMQZMmslD7jUb1BvBc%2B7cIJlYIwE8c8KpJApGCe2g9Ld2%5CL%2BysTvQ0WgMPtSrlpoEzAgWgC%5CsttMMTHD4W6dtD7RI01RKskuMBbowcx6jmit6ErmEspQpog2x%5COb1yk7QA7XKiSZs9uobjrB5IetUeG89uR%3A1697889605398; YD00517437729195%3AWM_NI=vvwX4ehyShYpEHQMMqlkNWLynRnejThr23Io1ADh9xmebnpMIlZU3ZAPP26%2FRZSPcRWFb8s8Se0Bl7ahXFv47NWdYXFflkxK1FdsqGY0eaC7I39PdibEEIZhzH%2BLiCy6Vm0%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee85f461ab95a7b1c46df39a8ab3c55a979b9bb0c162f28782b7cf6f8888bf87fc2af0fea7c3b92ab6aab9b9b76faca79d89dc7c87989faed07bb0b582b8cf73ae8ea286e960acaefed4cc65f39f8c89bc74afbbae8ff3478bb496b6b2528390a0d3b52592869db1e25a959aaed9f23491bb00a3ef3da3b898a7f540f5929985dc5486baa48cfb41f39aac94f44d9bf0ab82c23d8bedf7b1e763a29b8baad964ba98e5adec49bbea9a8eb337e2a3; YD00517437729195%3AWM_TID=bqNtTEkhOrhAQBVEQBOFy3JNRObWD%2Bfj; q_c1=9292243891aa4da48128d475a93cc0b4|1697888818000|1697888818000; z_c0=2|1:0|10:1698134261|4:z_c0|80:MS4xRTE0VVNRQUFBQUFtQUFBQVlBSlZUZlhHSkdhc0xsbG5KU0NCeWlMVkx0U3piWHF0T1ZfR21nPT0=|b7c6ebe1f9aa498533ae1c2252056c8d9fa2d6c96e3f60902b4162e79de523b3; _xsrf=0b449fcf-32d7-4988-99c4-3bb2bde5b240; tst=r; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1697888670,1698417665; SESSIONID=gJo8by3HENleMDuHltRAL1EvcPzh9PAafcJNsKSsYKI; JOID=UVsXBU6K5PlymmyuBY-yqu03_jwT7a-SSf4VnEnJqpQT1C7bTIstxRKcbasCAghVg-xe4MLoQV2S3yvr7WMa7TE=; osd=Wl8XBkuB4Plxn2eqBYy3oek3_TkY6a-RTPURnErMoZAT1yvQSIsuwBmYbagHCQxVgOlV5MLrRFaW3yju5mca7jQ=;KLBRSID={self.kession};unlock_ticket=ACDYY0WeIhcmAAAAYAJVTRjTO2UPlTz8J-IYfhzvPWAoiW1nCyA-Sg==; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1698417682",
            'Referer': 'https://www.zhihu.com/people/72-31-98-7/following',
            'X-Zse-93': '101_3_3.0',
            'X-Zse-96': x_zse_96,
            "X-zst-81": js_81
        }
        if (offset > 20):
            my_header[
                "Referer"] = f'https://www.zhihu.com/people/72-31-98-7/following?page={offset//20-1}'
        response = session.get(target_url, headers=my_header)
        response_v1 = session.post(
            "https://zhihu-web-analytics.zhihu.com/api/v2/za/logs/batch")
        response_v2 = session.post(
            "https://zhihu-web-analytics.zhihu.com/api/v3inv2/za/logs/batch")
        print("page:", offset/20)

        answers_list = response.json()
        data = answers_list["data"]

        for item in data:
            print(item["id"], item["name"])
            break
        self.kession = response.cookies["KLBRSID"]
        return self.kession

if __name__ == "__main__":
   
    d_c0 = "AICTUe2WlBePTrFSaV0AlIhdFAJwtto1Kr4=|1697888667"
    kession = "37f2e85292ebb2c2ef70f1d8e39c2b34|1698417680|1698417661"
    offset_list = [0, 20,60]
    for offset in offset_list:
        spider = ZhihuSpider(d_c0,kession)
        kession = spider.get_page(offset)
