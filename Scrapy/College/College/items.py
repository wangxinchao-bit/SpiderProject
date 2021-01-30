# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class CollegeItem(Item):
    # define the fields for your item here like:
    u_name = Field()
    u_location =Field()
    u_special =Field()
    u_type =Field()
    u_upper =Field()
    u_quantity =Field()
    u_website =Field()
