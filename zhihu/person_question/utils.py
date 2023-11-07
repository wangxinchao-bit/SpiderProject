

# coding=utf-8

import os
import re
import time
import random
import json
import requests
import hashlib
import execjs
import base64
import subprocess
from tqdm import tqdm

REG = re.compile('<[^>]*>')
session = requests.Session()

with open('js/X_zse_96.js', 'r', encoding='utf-8') as f:
    jstext = f.read()
ctx_96 = execjs.compile(jstext)

def get_x_zse_96(api, cookie_dc_2):
    ta = "101_3_3.0"
    tt_codes = ta +'+'+api+'+'+ cookie_dc_2
    hl = hashlib.md5()
    hl.update(tt_codes.encode('utf-8'))
    res_md5 = hl.hexdigest()
    result = ctx_96.call('func', res_md5)
    return result

def get_timestamp():
    return str(round(time.time()*1000))


REG = re.compile('<[^>]*>')

def extract_answer(s):
    data = s.replace("\\", "")
    # images_list = re.findall('img src="(http.*?)"', data, re.S)
    temp_list = REG.sub("", s).replace("\n", "").replace(" ", "")
    return temp_list
