
# coding=utf-8
import requests
import json
import re
import csv
import random
import time
import os
import base64
REG = re.compile('<[^>]*>')
import requests
import execjs
all_data = {}
def extract_answer(s):
    data = s.replace("\\", "")
    temp_list = REG.sub("", s).replace("\n", "").replace(" ", "")
    return temp_list

url = "https://www.zhihu.com/api/v4/members/72-31-98-7/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=0&limit=20"


with open('X_Zst81.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
    js_text = execjs.compile(js_code)
    js_81 = js_text.call('x_81')
    print(js_81)


with open('X_zse_96.js', 'r', encoding='utf-8') as f:
    js_code = f.read().replace('__xZst81', js_81)
    js_text = execjs.compile(js_code)
    js_96 = js_text.call('func')
    print(js_96)


data = {'gk_version': 'gz-gaokao',
        't': 'general',
        'q': '爬虫工程师',
        'correction': '1',
        'offset': '0',
        'limit': '20',
        'filter_fields': '',
        'lc_idx': '0',
        'show_all_topics': '0',
        'search_source': 'Normal'
        }
headers = {'Accept': '*/*',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-origin',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
          'x-api-version': '3.0.91',
          'x-app-za': 'OS=Web',
          'x-requested-with': 'fetch',
          'x-zse-93': '101_3_3.0',
          'x-zse-96': js_96,
          'x-zst-81': js_81,
          }

count = 0 
max_pages = 1
while True:
    text = requests.get(url = url,headers=headers).json()   

    print(text)

    break
  
# with open("data.json","w",encoding="utf-8") as file:
#     file.write(json.dumps(all_data,indent=4,ensure_ascii=False))


