# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    # 起始的URL地址(把第1页地址)
    start_urls = ['https://maoyan.com/board/4?offset=0']
    offset = 0

    def parse(self, response):
        # 基准xpath
        dd_list=response.xpath('//dl[@class="board-wrapper"]/dd')
        # for依次遍历
        for dd in dd_list:
            # 创建对象(类:items.py中的class MaoyanItem())
            item = MaoyanItem()
            # 电影名称
            item['name'] = dd.xpath('./a/@title').extract_first().strip()
            # 电影主演
            item['stars'] = dd.xpath('.//p[@class="star"]/text()').extract_first().strip()
            # 上映时间
            item['time'] = dd.xpath('.//p[@class="releasetime"]/text()').extract_first().strip()

            # 把爬取的数据交给管道文件pipeline处理
            yield item

        # 用于拼接新的URL交给调度器入队列
        self.offset += 10
        if self.offset <= 90:
            url = 'https://maoyan.com/board/4?offset={}'.format(self.offset)
            # 交给调度器入队列
            yield scrapy.Request(
                url = url,
                callback = self.parse
            )










