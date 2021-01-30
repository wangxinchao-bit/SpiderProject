# -*- coding: utf-8 -*-
import scrapy
import  json

from ..items import SoItem


class SoSpider(scrapy.Spider):
    name = 'so'
    allowed_domains = ['image.so.com']

    def start_requests(self):
        url = 'http://image.so.com/zjl?ch=beauty&sn={}&listtype=人人网登录&temp=1'
        # 生成5页的地址,交给调度器
        for i in range(5):
            sn = i*30
            full_url = url.format(sn)
            yield scrapy.Request(
                url = full_url,
                callback = self.parse_image,
                dont_filter=False
            )

    def parse_image(self,response):
        html = json.loads(response.text)
        # 提取图片链接
        for img in html['list']:
            item = SoItem()
            item['img_link'] = img['qhimg_url']

            yield item



