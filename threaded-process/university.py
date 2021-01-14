# -*- encoding = utf-8 -*-
import random
import os
import shutil
import requests
from lxml import etree
import multiprocessing
import csv

"""
@ mulitply multiprocessing spider  use process pool
@ author wxc
@ spider novels from the shuquge website 
"""

class novelSpider(object):
    def __init__(self,url,dir):
        self.ua_list =  [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
        ]
        self.url = url
        self.queue = multiprocessing.Manager().Queue()
        self.dir = "./"+dir+'/'
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        else :
            shutil.rmtree(self.dir)
            os.mkdir(self.dir)

    def producer(self):
        headers = {'User-Agent': random.choice(self.ua_list)}
        response = requests.get(url=self.url, headers=headers)
        html = etree.HTML(response.content.decode(encoding='gbk'))
        lists = html.xpath('//td[@align="center"]')
        for item in lists:
            try:
                province = item.xpath('a/span[@class="style12he"]/text()')[0]
                links = item.xpath('a/@href')[0]
                links =self.url + links
                self.queue.put((province,links))
            except:
                pass

    def consumer(self):
        while not self.queue.empty():
            chapter = self.queue.get()
            province = chapter[0]
            links = chapter[1]
            filename = self.dir + province + '.csv'

            if not os.path.exists(filename):
                f = open(filename, 'w', encoding='utf-8',newline="")
                csv_writer = csv.writer(f)
                csv_writer.writerow(["school", "website"])
                headers = {'User-Agent': random.choice(self.ua_list)}
                res = requests.get(url=links, headers=headers)
                html = etree.HTML(res.content.decode('gbk'))
                "[starts-with(@id,'fuck')]"
                school = html.xpath('//span[starts-with(@class,"STYLE")]')
                for item in school:
                    try:
                        name = item.xpath('a/text()')[0]
                        link = item.xpath('a/@href')[0]
                        csv_writer.writerow([name,link])
                    except:
                        pass
                f.close()
            else:
                print(filename + "have existed")



    def main(self):
        self.producer()
        # Asynchronous process pool (non-blocking)
        pool = multiprocessing.Pool(10)
        # The total number of processes maintained is 10.
        # When a process finishes executing, a new process will be started.
        for index in range(100):
            pool.apply_async(self.consumer)
        pool.close()
        pool.join()

if __name__ == '__main__':
    # please attentiom to the url form of novel form shuquge website
    Siper=novelSpider("http://u.feelingmsg.com/u/","University")
    Siper.main()

