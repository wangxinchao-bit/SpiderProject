# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

class DaomuPipeline:
    def process_item(self, item, spider):
        file="./小说/"+item["capter_name"]+"/"+item["volume_name"]+"/"
        if not os.path.exists(file):
            # 创建多层路径
            os.makedirs(file)
        fileName=file+item["zh_num"]+"-"+item["zh_name"]+".txt"
        with open( fileName,'w') as f:
            f.write(str(item["zh_content"]))
            f.close()

        return  item