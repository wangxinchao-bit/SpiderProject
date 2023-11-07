import requests
import json

headers = {
    "authority": "weibo.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
    "client-version": "v2.44.15",
    "referer": "https://weibo.com/u/2611607127",
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
    "login_sid_t": "ed5d051df60f05cedb1d633e2388c212",
    "cross_origin_proto": "SSL",
    "_s_tentry": "weibo.com",
    "Apache": "1786490439351.0962.1699198862904",
    "SINAGLOBAL": "1786490439351.0962.1699198862904",
    "ULV": "1699198862906:1:1:1:1786490439351.0962.1699198862904:",
    "appkey": "",
    "WBtopGlobal_register_version": "2023110523",
    "_ga_N7T0RGSEK2": "GS1.1.1699199601.1.0.1699199601.60.0.0",
    "__gpi": "UID=00000c806ff41b58:T=1699199598:RT=1699199598:S=ALNI_Mb-wzeQDuVZQ3lIzMd5GtuOrCDkOg",
    "_ga_HLZYVQ2W95": "GS1.1.1699199602.1.0.1699199602.0.0.0",
    "_ga_DL2CM4NHWS": "GS1.1.1699199602.1.0.1699199602.0.0.0",
    "_ga_TBFGB6E6C0": "GS1.1.1699199602.1.0.1699199602.0.0.0",
    "_ga": "GA1.2.2078800881.1699199602",
    "_gid": "GA1.2.2079526416.1699199603",
    "__gads": "ID=d121823b96df34a2-224ce1bc3ce500b2:T=1699199598:RT=1699199600:S=ALNI_Masir3w2zIw-NmRQUZNqefgXswQcg",
    "UOR": ",,www.baidu.com",
    "webim_unReadCount": "%7B%22time%22%3A1699199617912%2C%22dm_pub_total%22%3A2%2C%22chat_group_client%22%3A371%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A374%2C%22msgbox%22%3A0%7D",
    "SUBP": "0033WrSXqPxfM72wWs9jqgMF55529P9D9W5XM0MdZbb.dVjBZvKbgd9R5JpVF02N1h54eo-NS0BN",
    "SUB": "_2AkMSGzMkdcPxrAVYnvsQyW_la4RH-jyhzlrSAn7uJhMyAxh87mwMqSVutBF-XGYmEiWbLUnCf3RlTK1Zdf26O5y-",
    "wb_view_log": "1707*10671.5",
    "PC_TOKEN": "9e6c2e78c0",
    "WBPSESS": "Dt2hbAUaXfkVprjyrAZT_GdR2dzE8Cl64yGlfs90oQYjc7UKgVK05F8ZbERpfJWflT8FveVTMqJooz88U_V6xa_CffB_TPBVt6Xuo4Rdhlp5xK57kogY_Jbn8CI7l-yvP7y2Wd3BuDszbtwJEwWNkA=="
}
url = "https://weibo.com/ajax/statuses/mymblog"

page = 1
while True:

    params = {
        "uid": "2611607127",
        "page": f"{page}",
        "feature": "0"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(page)
    page +=1

    data = response.json()
    for item in data["data"]["list"]:
        print(item["text_raw"])