
# -*- encoding = utf-8 -*-
import requests
from lxml import etree
import csv
import json
import pymysql


class mysqlSpider(object):
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='mk47908493', port=3306, db='spider')
        self.cursor =self.db.cursor()

    def look_version(self):
        sql = 'select version()'
        self.cursor.execute('SELECT VERSION()')
        data = self.cursor.fetchone()
        print('Database version:', data)

    def create_database(self):
        sql = "CREATE DATABASE spiders DEFAULT CHARACTER SET utf8"
        self.cursor.execute(sql)

    def create_table(self):
        sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))'
        self.cursor.execute(sql)

    def search_info(self):
        sql = 'SELECT * FROM zhihuhotnews WHERE rank >= 20'
        try:
            self.cursor.execute(sql)
            print('Count:',   self.cursor.rowcount)

            # only the first search result
            # one = self.cursor.fetchone()
            # print('One:', one)

            # all the search result
            results = self.cursor.fetchall()
            print('Results:', results)

            # To access a detailed
            print('Results Type:', type(results))
            for row in results:
                print(row)

            #  Traversal access
            row = self.cursor.fetchone()
            while row:
                print('Row:', row)
                row = self.cursor.fetchone()

        except:
            print('Error')

    def delete_info(self):
        condition = 'rank>21'
        sql = 'DELETE FROM zhihuhotnews  WHERE {condition}'.format(condition=condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def update_info(self):
        data = {
                    "rank": "21",
                    "links": "https://www.zhihu.com/question/438546657",
                    "title": "sdfghjkl;"
                }

        table = 'zhihuhotnews'
        keys = ', '.join(data.keys())
        print(keys)
        values = ', '.join(['%s'] * len(data))
        print(values)
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                             values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        print(sql)
        try:
            if self.cursor.execute(sql, tuple(data.values()) * 2):
                print('Successful')
                self.db.commit()
        except:
            print('Failed')
            self.db.rollback()
        self.db.close()

    def main(self):
        # self.delete_info()
        # self.search_info()
        self.update_info()



if __name__ == '__main__':
    mysql = mysqlSpider()
    mysql.main()