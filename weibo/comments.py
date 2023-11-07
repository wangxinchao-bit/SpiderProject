import requests
import time
import random


headers = {
    "authority": "weibo.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
    "client-version": "v2.44.15",
    "referer": "https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F",
    "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "server-version": "v2023.11.3.2",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "mosU9mxBtVyUuncIihZUw99K"
}
cookies = {
    "XSRF-TOKEN": "mosU9mxBtVyUuncIihZUw99K",
    "SUB": "_2AkMSGzyif8NxqwFRmfoUzmPkZIlwywrEieKkR815JRMxHRl-yT9vqhJStRB6OZsSTVH4IhsS9i2cmAYY83YJQugyUJgm",
    "SUBP": "0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5wFUIZS1uy_hX5gfnf2Vho",
    "WBPSESS": "V0zdZ7jH8_6F0CA8c_ussXbZYD_K7wru8gstM2AhI317H3HYXhKlfO1di9RMZw8EeQvF1Me3_KteaLuTHH4GU1YLNrmpvd4ovJdpzyCLNhXihpkM9xCNGncwDEwx-zBBgP8GVq4N-slCxgFbWJxyOibtpqTFwfxoPSeu-9rpQC0="
}
url = "https://weibo.com/ajax/statuses/buildComments"

max_id = 0
while True:
    params = {
        "is_reload": "1",
        "id": "4958947259713897",
        "is_show_bulletin": "2",
        "is_mix": "0",
        "count": "20",
        "type": "feed",
        "uid": "3089788785",
        "fetch_level": "0",
        "locale": "en",
        "max_id": max_id
    }
    response = requests.get(url, headers=headers,
                            cookies=cookies, params=params)
    try:
        data = response.json()
        for item in data["data"]:
            print(item["id"], item["source"], item["text"])
        # print(response.json())
        max_id = data["max_id"]
        time.sleep(random.randint(1, 3))
    except:
        break

    #   username = '17809257747' # 微博账号
    #     password = 'zxcvBnm123@' # 微博密码
