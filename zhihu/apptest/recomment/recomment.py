
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

all_data = {}
def extract_answer(s):
    data = s.replace("\\", "")
    # images_list = re.findall('img src="(http.*?)"', data, re.S)
    temp_list = REG.sub("", s).replace("\n", "").replace(" ", "")
    return temp_list

url = "https://www.zhihu.com/api/v3/feed/topstory/recommend?action=down&ad_interval=-10&after_id=11&desktop=true&page_number=1&session_token=20feb002ad45970890afc37fc5182669"

count = 0 
max_pages = 10
while True:
    text = requests.get(url = url).json()
    for infos in text["data"]:
        item ={}
        item["id"] = infos["id"]
        item["created_time"] = infos["created_time"]
        try:
            item ["content"] =extract_answer(infos["target"]["content"])
        except:
            item ["content"] =" "
        all_data[item["id"]] = item
    if text["paging"]["is_end"]:
        break
    else:
        url = text["paging"]["next"]
    
    print(item)

    if(count> max_pages):
        break
    print(count)
    count +=1

with open("data.json","w",encoding="utf-8") as file:
    file.write(json.dumps(all_data,indent=4,ensure_ascii=False))


