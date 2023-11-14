# -*- coding: utf-8 -*-
import pickle
from threading import Thread
import time
import requests
from io import BytesIO
import os
from PIL import Image
requests.packages.urllib3.disable_warnings()

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
           'referer': 'https://www.zhihu.com/'}

class showpng(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        img = Image.open(BytesIO(self.data))
        img.show()


def islogin(session):
    try:
        session.cookies.load(ignore_discard=True)
    except Exception:
        pass
    loginurl = session.get(
        "https://www.zhihu.com/api/v4/me?include=visits_count", headers=headers).json()
    try:
        if loginurl['messages_count'] == 0:
            print('Cookies值有效，', loginurl['name'], '，已登录！')
            return session, True
        else:
            print('Cookies值已经失效，请重新扫码登录！')
            return session, False
    except:
        print('Cookies值已经失效，请重新扫码登录！')
        return session, False

def login():
    session = requests.session()
    if not os.path.exists('zhcookies.cookie'):
        with open('zhcookies.cookie', 'wb') as f:
            pickle.dump(session.cookies, f)

    session.cookies = pickle.load(open('zhcookies.cookie', 'rb'))
    session, status = islogin(session)
    if not status:
        session = requests.session()
        session.post('https://www.zhihu.com/udid', headers=headers)
        url = 'https://www.zhihu.com/api/v3/account/api/login/qrcode'
        login = session.post(url, headers=headers).json()
        token = login['token']
        tokenurl = 'https://www.zhihu.com/api/v3/account/api/login/qrcode/{}/image?utm_campaign=internal&utm_medium=qr&utm_source=login&utm_term=force_launch&utm_content=qrscand'
        png = session.get(tokenurl.format(token), headers=headers)
        t = showpng(png.content)
        t.start()
        dataurl = 'https://www.zhihu.com/api/v3/account/api/login/qrcode/{}/scan_info'
        while 1:
            data = session.get(dataurl.format(token), headers=headers).json()
            try:
                if '0' in str(data['status']):
                    print('二维码未失效，请扫码！')
                elif '1' in str(data['status']):
                    print('已扫码，请确认！')
                else:
                    break
            except:
                name = session.get(
                    'https://www.zhihu.com/api/v4/me?include=visits_count', headers=headers).json()
                print(name['name'], '登录成功！')
                break
            time.sleep(2)
        with open('login/zhcookies.cookie', 'wb') as f:
            pickle.dump(session.cookies, f)
    return session


if __name__ == '__main__':
    login()
