import requests
import json
import time
import random

class TencentSpider(object):
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0'}
        self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1563912271089&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1563912374645&postId={}&language=zh-cn'

    # 请求函数(两级页面都需要请求)
    def get_page(self,url):
        res = requests.get(url,headers=self.headers)
        res.encoding = 'utf-8'
        return json.loads(res.text)

    # 获取数据(名称 职责　要求)
    def get_data(self,html):
        job_info = {}
        for job in html['Data']['Posts']:
            job_info['job_name'] = job['RecruitPostName']
            post_id = job['PostId']
            two_url = self.two_url.format(post_id)
            job_info['job_duty'],job_info['require'] = \
                             self.parse_two_page(two_url)
            try :
                print(job_info)
            except:
                pass

    # 解析二级页面函数(职责 要求)
    def parse_two_page(self,two_url):
        two_html = self.get_page(two_url)
        duty = two_html['Data']['Responsibility']
        require = two_html['Data']['Requirement']
        return duty,require

    def main(self):
        for index in range(1,11):
            url = self.one_url.format(index)
            one_html = self.get_page(url)
            self.get_data(one_html)

            time.sleep(random.uniform(0.5,2))

if __name__ == '__main__':
    spider = TencentSpider()
    spider.main()












