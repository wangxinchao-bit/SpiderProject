
'''
   采用多线程进行博客园新闻
'''

import  requests
from lxml import etree
import os
import threading
import time
import  requests
from lxml import etree
import os
import re
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4270.0 Safari/537.36'
}
all_urls =[]
all_newurl=[]
all_file_path = []
g_lock = threading.Lock()


class Produce(threading.Thread):
    def run(self):

        global all_urls
        global all_newurl
        while len(all_urls) > 0:
            g_lock.acquire()  # 在访问all_urls的时候，需要使用锁机制
            page_url = all_urls.pop()  # 通过pop方法移除最后一个元素，并且返回该值
            g_lock.release()  # 使用完成之后及时把锁给释放，方便其他线程使用
            try:
                response = requests.get(url=page_url, headers=headers)
                html = etree.HTML(response.text)
                print(html)
                url_lists = html.xpath('//div[@id="news_list"]//div[@class="news_block"]')
                for item in url_lists:
                    news ={}
                    title = item.xpath('./div[@class="content"]/h2/a/text()')[0]
                    href = "https://news.cnblogs.com" + item.xpath('./div[@class="content"]/h2/a/@href')[0]
                    news["title"] =title
                    news ["url"] =href
                    all_newurl.append(news)

                time.sleep(0.5)
            except:
                pass


class  Consumer(threading.Thread):
    def run(self) :
        global all_newurl
        while len(all_newurl) > 0:
            g_lock.acquire()  # 在访问all_urls的时候，需要使用锁机制
            newInfo = all_newurl.pop()  # 通过pop方法移除最后一个元素，并且返回该值
            g_lock.release()  # 使用完成之后及时把锁给释放，方便其他线程使用
            response = requests.get(url=newInfo["url"],headers=headers)

            if(response.status_code==200):
                html = response.text
                all_path = "./news/html/"
                if not os.path.exists(all_path):
                    os.makedirs(all_path)
                try:
                    path = all_path+newInfo["title"]+".html"
                    with open(path,'w',encoding='utf-8') as f:
                        f.write(html)
                except:
                    pass


class paraseDataHtml(threading.Thread):

    def run(self):
        global all_file_path
        while len(all_file_path) > 0:
            g_lock.acquire()  # 在访问all_urls的时候，需要使用锁机制
            path  = all_file_path.pop()  # 通过pop方法移除最后一个元素，并且返回该值
            g_lock.release()  # 使用完成之后及时把锁给释放，方便其他线程使用

            f = open(path,'r',encoding='UTF-8')
            res =f.read()
            html = etree.HTML(res)
            try:
                newList = html.xpath('//div[@id="news_main"]')[0]
                title =newList.xpath('./div[@id="news_title"]/a/text()')[0]
                conttext =newList.xpath('./div[@id="news_content"]/div[@id="news_body"]//p/text()')
                newInfomation = ''
                for item in conttext:
                    newInfomation+=item
                newInfomation= newInfomation.strip().replace(u'\u3000', '').replace('\xa0', u'')

                all_path = "./news/md/"
                if not os.path.exists(all_path):
                    os.makedirs(all_path)
                mdpath =all_path + title+'.md'
                with open(mdpath,'w') as f:
                    f.write(newInfomation)
            except:
                pass

if __name__=="__main__":

    for i in range(5):
        url = "https://news.cnblogs.com/n/page/{}/".format(i)
        all_urls.append(url)
    print(all_urls)

    # 生产者
    newList=[]
    for x in range(10):
        down = Produce()
        down.start()
        newList.append(down)
    for t in newList:
        t.join()


    # 消费者
    newList=[]
    for x in range(10):
        down = Consumer()
        down.start()
        newList.append(down)
    for t in newList:
        t.join()



    filePath = './news/html/'
    pathList = os.listdir(filePath)
    print(pathList)

    for item in pathList:
        path = filePath + item
        all_file_path.append(path)
    newList=[]
    for x in range(10):
        down = paraseDataHtml()
        down.start()
        newList.append(down)
    for t in newList:
        t.join()