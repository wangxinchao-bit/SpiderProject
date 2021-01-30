# -*- coding: UTF-8 -*-
# @author: zhulw
# @file: login_test
# @time: 2020/12/22
# @desc:

import cv2
import execjs
import requests
from lxml import etree


class Login:
    def __init__(self, username="2018302130141", password="02027x"):
        self.session = requests.session()
        self.session.headers = {
            "Host": "seat.lib.whu.edu.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        }
        self.username = username
        self.password = password
        self.set_cookie_url = "https://seat.lib.whu.edu.cn/login?targetUri=%2F"
        self.captcha_img_url = "https://seat.lib.whu.edu.cn/cap/captcha"
        self.img_url = "https://seat.lib.whu.edu.cn/cap/captchaImg?token={}"
        self.check_url = "https://seat.lib.whu.edu.cn/cap/checkCaptcha"
        self.login_url = "https://seat.lib.whu.edu.cn/auth/signIn"
        self.search_url = "https://seat.lib.whu.edu.cn/freeBook/ajaxSearch?onDate=2020-12-22&building=null&room=null&hour=null&startMin=null&endMin=null&power=null&window=null"

    def get_captcha_image(self):
        res = self.session.get(self.set_cookie_url)
        html = etree.HTML(res.text)
        SYNCHRONIZER_TOKEN = html.xpath('//input[@name="SYNCHRONIZER_TOKEN"]/@value')[0]
        response = self.session.get(url=self.captcha_img_url)
        token = response.json()["token"]
        data = response.json()["data"]
        print(data)
        r = self.session.get(self.img_url.format(token))
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
        return SYNCHRONIZER_TOKEN, token, data

    @staticmethod
    def get_strapp():
        img = cv2.imread('captcha.jpg')
        a = []
        b = []

        def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                xy = "%d,%d" % (x, y)
                a.append(x)
                b.append(y)
                cv2.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
                cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                            1.0, (0, 0, 0), thickness=1)
                cv2.imshow("image", img)

        cv2.namedWindow("image")
        cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
        cv2.imshow("image", img)
        cv2.waitKey(0)
        img[b[0]:b[1], a[0]:a[1], :] = 0  # 注意是 行，列（y轴的，X轴）
        cv2.imshow("image", img)
        cv2.waitKey(0)
        strapp = '[{"x":' + str(a[0]) + ',"y":' + str(b[0]) + '},{"x":' + str(a[1]) + ',"y":' + str(
            b[1]) + '},{"x":' + str(
            a[2]) + ',"y":' + str(b[2]) + '}]'
        return strapp

    @staticmethod
    def get_a(strapp):
        et = execjs.compile("""
            function code(s, discard, alpha, beta, w1, w2) {
            s = String(s);
            var buffer = 0
                , i = 0
                , length = s.length
                , result = ''
                , bitsInBuffer = 0;
            while (i < length) {
                var c = s.charCodeAt(i);
                c = c < 256 ? alpha[c] : -1;
                buffer = (buffer << w1) + c;
                bitsInBuffer += w1;
                while (bitsInBuffer >= w2) {
                    bitsInBuffer -= w2;
                    var tmp = buffer >> bitsInBuffer;
                    result += beta.charAt(tmp);
                    buffer ^= tmp << bitsInBuffer;
                }
                ++i;
            }
            if (!discard && bitsInBuffer > 0)
                result += beta.charAt(buffer << (w2 - bitsInBuffer));
            return  result + '===='.slice((result.length % 4) || 4);;
        }
        """)
        beta = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        Array = []
        for i in range(0, 256):
            Array.append(i)
        a = et.call('code', strapp, False, Array, beta, 8, 6)
        print(a)
        return a

    def login(self, SYNCHRONIZER_TOKEN, token):
        data = {
            "SYNCHRONIZER_TOKEN": SYNCHRONIZER_TOKEN,
            "SYNCHRONIZER_URI": "/login",
            "username": self.username,
            "password": self.password,
            "authid": token
        }
        response = self.session.post(self.login_url, data=data)
        # print(response.text)

    def check_captcha(self, a, token):
        params = {
            "a": a,
            "token": token,
            "userId": "",
        }
        response = self.session.get(self.check_url, params=params)
        print(response.text)

    def getSeatInfo(self):
        response = self.session.get(self.search_url)
        print(response.text)

    def run(self):
        SYNCHRONIZER_TOKEN, token, data = self.get_captcha_image()
        strapp = self.get_strapp()
        a = self.get_a(strapp)
        self.check_captcha(a, token)
        self.login(SYNCHRONIZER_TOKEN, token)
        self.getSeatInfo()


if __name__ == '__main__':
    Login().run()
