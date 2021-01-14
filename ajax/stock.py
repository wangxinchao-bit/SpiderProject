from urllib.parse import urlencode
import requests
import  json
from pyquery import PyQuery as pq

class stockSpider(object):
    def __init__(self):
        self.headers = {
                            'Host': 'query.sse.com.cn',
                            'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
                        }

    def get_page(self,page):
        url = "http://query.sse.com.cn/security/stock/getStockListData2.do?&jsonCallBack=jsonpCallback40435&isPagination=true&stockCode=&csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp.beginPage=2&pageHelp.pageSize=25&pageHelp.pageNo=2&pageHelp.endPage=21&_=1598719271166"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except requests.ConnectionError as e:
            print('Error', e.args)

    def main(self):
        text = self.get_page(1)
        data = json.loads(text[19:-1])
        r_list = data["pageHelp"]["data"]
        for item in r_list:
            COMPANY_CODE = item["COMPANY_CODE"]
            COMPANY_ABBR = item["COMPANY_ABBR"]
            QIANYI_DATE = item["QIANYI_DATE"]
            print(COMPANY_ABBR, COMPANY_CODE, QIANYI_DATE)

if __name__ == '__main__':
    stock = stockSpider()
    stock.main()
