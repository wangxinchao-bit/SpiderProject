# -*- coding: utf-8 -*-
import scrapy
from fake_useragent import UserAgent
ua =UserAgent().random
import json


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['http://www.bilibili.com/']

    def start_requests(self):
        url ="http://api.bilibili.com/x/space/acc/info?mid={}"
        for i in range(1,10000):
            full_url =url.format(i)
            headers = {'User-Agent': ua,
                       'origin': 'http://space.bilibili.com',
                       'Upgrade-Insecure-Requests': '1',
                       'Host': 'api.bilibili.com',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                      }
            yield scrapy.Request(
                url=full_url,
                headers=headers,
                callback=self.parse_html
            )

    def parse_html(self, response):
        data =response.text
        try:
            item = json.loads(data)["data"]
            print(item)
            yield item
        except:
            pass
