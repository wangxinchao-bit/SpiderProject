# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan3'
    allowed_domains = ['maoyan.com']

    # 重写start_requests()方法,把所有URL地址都交给调度器
    # 去掉start_urls
    def start_requests(self):
        for offset in range(0,91,10):
            url = 'https://maoyan.com/board/4?offset={}'.format(offset)
            # 交给调度器
            yield scrapy.Request(
                url = url,
                callback = self.parse_html
            )

    def parse_html(self,response):
        # 基准xpath
        dd_list=response.xpath('//dl[@class="board-wrapper"]/dd')
        # for依次遍历
        for dd in dd_list:
            # 创建对象(类:items.py中的class MaoyanItem())
            item = MaoyanItem()
            # 电影名称
            item['name'] = dd.xpath('./a/@title').extract_first().strip()
            # 电影主演
            item['star'] = dd.xpath('.//p[@class="star"]/text()').extract_first().strip()
            # 上映时间
            item['time'] = dd.xpath('.//p[@class="releasetime"]/text()').extract_first().strip()
            # 把爬取的数据交给管道文件pipeline处理
            # print(item)
            yield item











