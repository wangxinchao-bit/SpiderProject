# -*- coding: utf-8 -*-
import json
import requests
import binascii
from Crypto.Cipher import AES

import json

import execjs
import requests
import random
import time

import execjs
with open('test.js', 'r', encoding='utf-8') as f:
    jstext = f.read()
ctx = execjs.compile(jstext)

def main():
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://jzsc.mohurd.gov.cn/home",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "accessToken": "",
        "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "timeout": "30000",
        "v": "231012"
    }
    cookies = {
        "Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c": "1699191297",
        "Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c": "1699191297"
    }
    url = "https://jzsc.mohurd.gov.cn/APi/webApi/asite/credit/record/query"

    for page in range(0,3):
        params = {
            "pg": f"{page}",
            "pgsz": "15",
        }
        print(page)
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        decrypted_data = response.text
        decrypted_data = str(decrypted_data)
        result = ctx.call('getDecryptedData', decrypted_data)
        print(result)
        time.sleep(random.randint(3,5))

if __name__ == '__main__':
    main()
        
        
