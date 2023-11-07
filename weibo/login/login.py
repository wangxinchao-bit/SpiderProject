
#  参考以下两个教程和代码
# 
# https://blog.csdn.net/a20100997/article/details/116781819?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522169921421116800213022750%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=169921421116800213022750&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-1-116781819-null-null.nonecase&utm_term=python%20%E7%88%AC%E8%99%AB%E7%99%BB%E5%BD%95&spm=1018.2226.3001.4450
# https://github.com/naiveliberty/WeiBo_Login/blob/master/weibo.py


import json
from urllib.parse import quote_plus

import binascii
import http.cookiejar

import xlwt
from bs4 import BeautifulSoup


import random
import re
import time
import math

import os
import requests
import base64
from urllib import parse
from binascii import b2a_hex
import ddddocr
import urllib.parse
ocr = ddddocr.DdddOcr()
import rsa

# 获取当前时间（毫秒）的Unix时间戳
def getTimeStamp():
    return str(int(time.time() * 1000))

def save_cookies_lwp(cookiejar, filename):

    cookies_dict = requests.utils.dict_from_cookiejar(cookiejar)
    # print(cookies_dict)
    # if not os.path.exists(filename):
    file = open(filename, 'w')
    # file.write('#LWP-Cookies-2.0')
    file.write(json.dumps(cookies_dict))
    file.close()

class Weibo():
    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.cookie_file = './cookie.json'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }
        self.session.headers.update(self.headers)
        self.agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
   
        # 登录前获取加密参数
        self.prelogin = self.get_server_data(self.get_su())

        print(self.prelogin)


    # 生成 Nonce
    def makeNonce(self):
        x = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        nonce_str = ""
        for i in range(6):
            index_num = int(math.ceil(random.random() * 1000000) % len(x))
            nonce_str += x[index_num]
        return nonce_str

    # 处理 username
    def get_su(self):
        username_quote = quote_plus(self.username)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    # 处理 password
    def process_password(self):
        passwd = "\t".join([str(self.prelogin["servertime"]), str(self.prelogin["nonce"])]) + "\n" + self.password
        return passwd

    # 获取加密参数
    def get_server_data(self, su):
        referer = 'https://weibo.com/'  # 注意必须加在请求头上，不然报错
        headers = {'User-Agent': self.agent, 'Referer': referer}

        pre_url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
        pre_url = pre_url + su + "&rsakt=mod&client=ssologin.js(v1.4.15)&_="
        pre_url = pre_url + getTimeStamp()
        pre_data_res = self.session.get(pre_url, headers=headers)

        sever_data = eval(
            pre_data_res.content.decode("utf-8").replace(
                "sinaSSOController.preloginCallBack", ''))
        return sever_data

    # 生成加密密码
    def get_encrypted_pwd(self):
        pubkey = rsa.PublicKey(int(self.prelogin["pubkey"], 16), int("10001", 16))
        return b2a_hex(rsa.encrypt(self.process_password().encode(), pubkey))

    def login(self):
        
        type = 2
        params = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "0",
            "qrcode_flag": "false",
            "useticket": "1",
            "pagerefer": "https://login.sina.com.cn/crossdomain2.php?action=logout&r=https://weibo.com/logout.php?backurl=/",
            "vsnf": "1",
            "su": self.get_su(),
            "service": "miniblog",
            "servertime": self.prelogin["servertime"],
            "nonce": self.prelogin["nonce"],
            "pwencode": "rsa2",
            "rsakv": self.prelogin["rsakv"],
            "sp": self.get_encrypted_pwd(),
            "sr": "1920*1080",
            "encoding": "UTF-8",
            "prelt": "431",
            "url":"https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype": "TEXT"
        }

        #  获取验证码操作
        url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
        pin_code = self.get_cap(self.prelogin["pcid"])

        params["pcid"] = self.prelogin["pcid"]
        params["door"] = pin_code
            # login_response = self.session.post(url=url, data=params, headers=self.headers)
        login_response = self.session.post(url=url, data=params, headers=self.headers)
        print(login_response.json())
        if "2070" in login_response.text:
            self.login()
        else:
            print(login_response.text)
            print(self.session.cookies)
            content = json.loads(login_response.text)
            protection_url = content['protection_url']
            protection_url_unquote = urllib.parse.unquote(protection_url)
            index_of_token = protection_url_unquote.find('token=')
            token = protection_url_unquote[index_of_token + 6:]
            print(token)

        
        retcode = -1  # 记录返回情况
        msg = ''
        redirect_url = ''
        # 短信验证码登录
        if type == 1:
            # 发送get请求，并解析结果，获得加密后的电话号码
            protection_url = 'https://login.sina.com.cn/protection/index?callback_url=http://login.sina.com.cn/&token=' + token
            protection_url_res = self.session.get(protection_url).text
            protection_url_res_bs = BeautifulSoup(protection_url_res, 'html.parser')
            encrypt_mobile = protection_url_res_bs.find(id='ss0').get('value')

            # 构造发送短信的请求
            send_message_url = 'https://login.sina.com.cn/protection/mobile/sendcode?token=' + token

            referer = "https://login.sina.com.cn/protection/index?token={}&callback_url=http%3A%2F%2Flogin.sina.com.cn%2F".format(
                token)
            headers = {
                'Referer': referer,
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"
            }

            body = {'encrypt_mobile': encrypt_mobile}
            data = urllib.parse.urlencode(body)
            # 发送验证码到手机
            res = self.session.post(send_message_url, headers=headers, data=data)

            message_code = input('输入短信验证码')

            login_url = 'https://login.sina.com.cn/protection/mobile/confirm?token=' + token
            login_post_data = {'encrypt_mobile': encrypt_mobile, 'code': message_code}

            login_post_res = self.session.post(login_url, headers=headers, data=login_post_data)
            login_post_res_json = json.loads(login_post_res.text)
            retcode = login_post_res_json.get('retcode')
            msg = login_post_res_json.get('msg')
            redirect_url = login_post_res_json.get('data').get('redirect_url')
        elif type == 2:
            privatemsg_url = 'https://login.sina.com.cn/protection/privatemsg/send'

            body = {'token': token}
            referer = 'https://login.sina.com.cn/protection/index?token={}&callback_url=http%3A%2F%2Flogin.sina.com.cn%2F'.format(
                token)
            headers = {
                'Referer': referer,
                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'login.sina.com.cn',
                'User-Agent': self.agent
            }
            data = urllib.parse.urlencode(body)
            html = requests.post(privatemsg_url, headers=headers, data=data)
            bs = BeautifulSoup(html.text, 'html.parser')
            res_json = json.loads(bs.text)
            retcode = res_json.get('retcode')
            msg = res_json.get('msg')
        if retcode == 20000000:
            # 如果是发送私信验证，需要主动调用接口获得redirect_url
            if (type == 2):
                stop = False
                getStatus_url = 'https://login.sina.com.cn/protection/privatemsg/getstatus'
                body = {'token': token}
                data = urllib.parse.urlencode(body)
                count = 0  # 尝试10次
                while (not stop):
                    time.sleep(2)  # 每2秒请求一次
                    html = requests.post(getStatus_url, data=data, headers=headers)
                    ret_json = json.loads(html.text)
                    redirect_url = ret_json.get('data').get('redirect_url')
                    count += 1
                    if (redirect_url != '' or count > 10):
                        stop = True
                if (redirect_url == ''):
                    print('未能在时间内正确发送私信验证！登陆失败！')
                    return

            # 登陆成功后跳转
            redirect_html = self.session.get(redirect_url)
            print(redirect_html)
            redirect_html_bs = BeautifulSoup(redirect_html.content.decode('ISO-8859-1'), 'html.parser')
            print(redirect_html_bs)
            location_replace = redirect_html_bs.find('script').contents[0].strip()
            location_replace_url = location_replace[18:-3]
            print(location_replace_url)
            data_res = self.session.get(location_replace_url)
            print("返回的结果信息")
            print(data_res.text)
            print("登录成功！")
            #  保存cookies 
            save_cookies_lwp(self.session.cookies, self.cookie_file)
            print(self.session.cookies)
        else:
            print(msg)
            return token
    def get_search(self):
        headers = headers = {
            "authority": "weibo.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
            "origin": "https://s.weibo.com",
            "referer": "https://s.weibo.com/",
            "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        res = self.session.get(url ="https://weibo.com/ajax/side/search?q=%E7%88%B1%E5%AD%A6%E4%B9%A0",
        headers = headers
        )
        print(res.text)

    def get_cap(self, pcid):
        # 需要输入验证码重新发送
        pimg_url = "https://login.sina.com.cn/cgi/pin.php?r=" + str(random.randint(0, 99999999)).zfill(8) + "&s=0&p=" + pcid
        img = self.session.get(pimg_url, headers=self.headers).content

        with open('./a.png', 'wb') as fp:
            fp.write(img)
        # with open('a.png', 'rb') as f:
        #     img_bytes = f.read()
        # res = ocr.classification(img_bytes)
        # print('识别出的验证码为：' + res)
        # post_data["door"]  = res
        # post_data_res = self.session.post(url, data=post_data, headers=headers)
        # print(post_data_res)
        # token = self.get_token(post_data_res)
        # print(token)
        pin_code = input("请输入验证码:")
        return pin_code


        filename = os.path.dirname(__file__) + "/weibo_pinimges/code.jpg"
        with open(filename, "wb") as f:
            f.write(img.content)
        # 验证码下载完毕
        pin_code = input("请输入验证码:")
        return pin_code


if __name__ == "__main__":
    user_info = {"username":"17809257747","password":"zxcvBnm123@"}
    weibo = Weibo(**user_info)
    weibo.login()

