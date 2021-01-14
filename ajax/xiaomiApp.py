

import requests
import json

class xiaomiAppSpider(object):

    def __init__(self):

        self.baseUrl ="https://app.mi.com/categotyAllListApi?page={}&categoryId=5&pageSize=30"
        self.header ={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Cookie": "JSESSIONID=aaaDXmSKiSlcv5845CxBx; __utma=127562001.895749513.1610637011.1610637011.1610637011.1; __utmb=127562001.4.10.1610637011; __utmc=127562001; __utmz=127562001.1610637011.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_765fefc2c357bae3970cea72e714811b=1610637011; Hm_lpvt_765fefc2c357bae3970cea72e714811b=1610637051; t_id=noimeiweb_240a8df6-ebeb-4c86-9828-700f2b6dd2ef",
            "Host": "app.mi.com",
            "Referer": "https://app.mi.com/category/5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
            "X-Requested-With": "XMLHttpRequest" }
        self.list_app =[]

    def get_page(self,url):
        url ="https://app.mi.com/categotyAllListApi?page=0&categoryId=5&pageSize=30"
        res = requests.get(url=url,headers =self.header)
        data = json.loads(res.text)
        app_list = data["data"]
        for item in app_list:
            self.list_app.append(item)

    def main(self):
        for i in range(1,60):
            print("%s page have crawled"%i)
            url = self.baseUrl.format(i)
            self.get_page(url)
        file = open('xmApp.json', 'a+', encoding='gbk')
        file.write(json.dumps(self.list_app, indent=2, ensure_ascii=False))
        file.close()
if __name__ == '__main__':
    xiaomiApp =xiaomiAppSpider()
    xiaomiApp.main()
