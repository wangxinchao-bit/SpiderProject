# -*- coding: utf-8 -*-
import scrapy
from ..items import CollegeItem

class CollegeSpider(scrapy.Spider):
    name = 'college'
    allowed_domains = ['college.gaokao.com']
    start_urls = ['http://college.gaokao.com/schlist/a1/']

    def parse(self, response):
        url_list=response.xpath('//div[@class="menufix"]/p/a/@href').extract()
        for url in url_list[1:35]:
            yield scrapy.Request(
                url = url,
                callback = self.parse_html_2
            )

    def parse_html_1(self, response):
        Number = response.xpath('//*[@id="qx"]/text()').get().split('/')[1][0]
        if Number =='页':
            Number='1'
        for ix in range(1,int(Number)+1):
            url=response.request.url+"p{}/".format(ix)

            yield scrapy.Request(
                url=url,
                callback=self.parse_html_2
            )

    def parse_html_2(self, response):
        # 基准xpath
        item=CollegeItem()
        dd_list = response.xpath('//div[@class="scores_List"]//dl')
        for dd in dd_list:
            # img=dd.xpath('./dt/a/@href').get()
            item["u_name"]=dd.xpath('./dt/strong/@title').get()
            SChool = dd.xpath('./dd/ul//li')
            Info_school=''
            for info in SChool:
                Info_school+=info.xpath('./text()').get()+" "
            Info =Info_school.split()

            item["u_location"]=Info[0].split('：')[-1]
            item["u_special"]=Info[1].split('：')[-1]
            item["u_type"]=Info[2].split('：')[-1]
            item["u_upper"]=Info[3].split('：')[-1]
            item["u_quantity"]=Info[4].split('：')[-1]
            item["u_website"]="".join(tuple(Info[5].split('：')[1:]))


            # 只有yield 才能 -o csv
            yield item




