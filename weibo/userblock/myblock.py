import requests


headers = {
    "authority": "weibo.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
    "client-version": "v2.44.15",
    # "referer": "https://weibo.com/u/6963554779",
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
    "SUB": "_2A25ITdJMDeRhGeBH7VEU9SrLzDWIHXVrO0SErDV_PUNbm9ANLUvwkW9NQag__jD9msPLg-s12mu6zXsfa52f3yPu",
 }
url = "https://my.sina.com.cn/?sudaref=weibo.com&display=0&retcode=0"
session  = requests.Session()
session.cookies.update(cookies)
response = session.get(url, headers=headers)
print(response.content.decode("utf-8"))


