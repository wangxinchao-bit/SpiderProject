import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from pymongo import MongoClient

class weiboSpider(object):

    def __init__(self):
        self.base_url  = 'https://m.weibo.cn/api/container/getIndex?'
        self.headers  = {
                            'Host': 'm.weibo.cn',
                            'Referer': 'https://m.weibo.cn/u/2830678474',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                            'X-Requested-With': 'XMLHttpRequest',
        }
        self.db = MongoClient()['weibo']
        self.collection =self.db['weibo']
        self.max_page = 10

    def get_page(self,page):
        params = {
            'type': 'uid',
            'value': '2830678474',
            'containerid': '1076032830678474',
            'page': page
        }
        try:
            response = requests.get(self.base_url, headers=self.headers,params=params)
            if response.status_code == 200:
                return response.json(), page
        except requests.ConnectionError as e:
            print('Error', e.args)

    def parse_page(self,json, page: int):
        if json:
            items = json.get('data').get('cards')
            for index, item in enumerate(items):
                if page == 1 and index == 1:
                    continue
                else:
                    item = item.get('mblog', {})
                    weibo = {}
                    weibo['id'] = item.get('id')
                    weibo['text'] = pq(item.get('text')).text()
                    weibo['attitudes'] = item.get('attitudes_count')
                    weibo['comments'] = item.get('comments_count')
                    weibo['reposts'] = item.get('reposts_count')
                    yield weibo

    def main(self):
        for page in range(1, self.max_page + 1):
            post_list =[]
            json = self.get_page(page)
            try:
                results = self.parse_page(*json)
                for item in results:
                    post_list.append(item)
            except:
                pass
            res = self.collection.insert_many(post_list)

if __name__ == '__main__':
    weibo = weiboSpider()
    weibo.main()
