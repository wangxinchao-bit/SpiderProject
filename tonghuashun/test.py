import json
import urllib3
import requests
import ddddocr
from loguru import logger
urllib3.disable_warnings()


def slide():
    session=requests.Session()
    session.verify=False
    session.headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Referer": "https://upass.10jqka.com.cn/",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
    params = {
        "captcha_type": "4",
        "appid": "registernew",
        "random": "396686007781.39954",
        "callback": "PreHandle"
    }
    response = session.get(url = "https://captcha.10jqka.com.cn/getPreHandle",  params=params).text
    json_data=json.loads(response[10:-1])['data']
    logger.debug(f'data：{json_data}')
    inity=json_data['inity']
    imgs=json_data['imgs']
    sign=json_data['sign']
    urlParams=json_data['urlParams']
    bg_url='https://captcha.10jqka.com.cn/getImg?'+urlParams+'&iuk='+imgs[0]
    bg_bytes=requests.get(url=bg_url).content
    with open("bg.jpg",'wb')as f:
        f.write(bg_bytes)
    slide_url='https://captcha.10jqka.com.cn/getImg?'+urlParams+'&iuk='+imgs[1]
    slide_bytes=requests.get(url=slide_url).content
    with open("slide.jpg",'wb')as f:
        f.write(slide_bytes)
    # ocr=ddddocr.DdddOcr()
    ocr = ddddocr.DdddOcr(det=False, ocr=False)

    dis=ocr.slide_match(slide_bytes,bg_bytes)
    logger.debug(f'dis：{dis}')
    x=str(int(int(dis['target'][0])/340*309))
    inity=str(int(inity)/340*309)
    verify_url="https://captcha.10jqka.com.cn/getTicket" + "?" + urlParams + "&phrase=" + (x) + ";" + inity + ";" + '309' + ";" + '177.22058823529412&callback=verify'
    logger.debug(f'verify_url：{verify_url}')
    response=session.get(url=verify_url).text
    logger.debug(response)
 
if __name__ == '__main__':
    slide()