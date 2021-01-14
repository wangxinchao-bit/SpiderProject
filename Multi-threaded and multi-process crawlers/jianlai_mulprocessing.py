# -*- encoding = utf-8 -*-

import random
import os
import shutil
import requests
from lxml import etree
import multiprocessing


"""
@ mulitply multiprocessing spider 

@ author wxc
@  spider novels from the shuquge website 
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
        html = etree.HTML(response.content.decode(encoding='utf-8'))
        lists = html.xpath('//div[@class="listmain"]/dl/dd')
        for item in lists:
            try:
                title = item.xpath('a/text()')[0]
                links = item.xpath('a/@href')[0]
                links = self.url + links
                self.queue.put((title, links))
            except:
                pass

    def consumer(self):
        while not self.queue.empty():
            chapter = self.queue.get()
            title = chapter[0]
            links = chapter[1]
            filename = self.dir + title + '.md'
            if not os.path.exists(filename):
                headers = {'User-Agent': random.choice(self.ua_list)}
                res = requests.get(url=links, headers=headers)
                html = etree.HTML(res.content.decode('utf-8'))
                text = html.xpath('//div[@id="content"]/text()')
                chapter = ''
                for paragraph in text:
                    chapter += paragraph.strip()
                    chapter += "\n"
                try:
                    with open(filename, 'w') as f:
                        f.write(chapter)
                        f.close()
                    print(title + 'has successfuly written!')
                except:
                    pass
            else:
                print(filename + "have existed")


    def main(self):
        self.producer()
        pool = multiprocessing.Pool(10)  # 异步进程池（非阻塞）
        for index in range(100):
            pool.apply_async(self.consumer)  # 维持执行的进程总数为10，当一个进程执行完后启动一个新进程.
        pool.close()
        pool.join()

if __name__ == '__main__':
    # please attentiom to the url form of novel form shuquge website
    Siper=novelSpider("http://www.shuquge.com/txt/8659/","tst")
    Siper.main()

