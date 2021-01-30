from scrapy import  cmdline

cmdline.execute('scrapy crawl bilibili -o userInfo.csv '.split())