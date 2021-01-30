from scrapy import cmdline

# cmdline.execute('scrapy crawl maoyan -o manyan.csv'.split())
cmdline.execute('scrapy crawl college -o name.csv'.split())