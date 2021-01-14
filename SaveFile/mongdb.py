
# -*- encoding = utf-8 -*-
import requests
from lxml import etree
import csv
import json
import pymysql
import pymongo

class mysqlSpider(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.Spider
        self.collection = self.db.zhihuHotnews

    def find_info(self):
        # find_one 's result is the dict
        result = self.collection.find_one({'rank': '1'})
        print(result)
        # find's result are a Cursor
        result = self.collection.find({'rank': '1'})
        print(result)
        for item in result:
            print(item)

    def remove_info(self):
        result = self.collection.remove({'rank': '1'})
        print(result)


    def main(self):
        self.find_info()
        self.remove_info()
        self.find_info()

if __name__ == '__main__':
    mysql = mysqlSpider()
    mysql.main()