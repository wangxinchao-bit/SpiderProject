
import requests
import json
from datetime import datetime
import os
import sys

def get_curday_hotnews():
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
    data = requests.get(url=url).json()
    all_hotnews = {}
    count = 0
    try:
        for item in data["data"]:
            item = item["target"]
            new_info = {}
            new_info["title"] = item["title_area"]["text"]
            new_info["hotspots"] = item["metrics_area"]["text"]
            new_info["link"] = item["link"]["url"]
            new_info["image_url"] = item["image_area"]["url"]
            all_hotnews[str(count)] = new_info
            count += 1
    except:
        for item in data["data"]:
            new_info = {}
            new_info["title"] = item["target"]["title"]
            new_info["url"] = item["target"]["url"]
            all_hotnews[str(count)] = new_info
            count += 1
    else:
        pass

    date = datetime.now()
    file_name = str(date.month) + "_" + str(date.day)
    with open(f"{file_name}.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(all_hotnews, ensure_ascii=False))

if __name__ == "__main__":
    get_curday_hotnews()
