import requests
from lxml import etree
import json

url ="http://www.ahtba.org.cn/site/trade/affiche/gotoTradeList?tradeType=01&classify=A&affiche=A04"

session =requests.session()
headers ={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding':'gzip,deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'www.ahtba.org.cn',
'Referer':'http://www.ahtba.org.cn/',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0(Linux;Android6.0;Nexus5Build/MRA58N)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.88MobileSafari/537.36'
}
session.headers =headers

res=  session.get(url =url)
print(res.status_code)
html = etree.HTML(res.text)
res_list = html.xpath('//div[@class="titBox"]')
for item in res_list:
    link = item.xpath('div/a/@href')[0]
    text = item.xpath('div/a/text()')[0]
    date = item.xpath('div[@class="fr nums"]/text()')[0]
    print(date,link,text)

url_2= "http://www.ahtba.org.cn/site/trade/affiche/pageList"
for i in range(1,1000):
    data ={"pubTime":"","tradeType":"01","tradeClassify":"A","afficheType":"A04","regionCode":"","afficheSourceType":"","afficheTitle":"","pageNum":i,"pageSize":10}
    headers ={
    'Accept':'*/*',
    'Accept-Encoding':'gzip,deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'154',
    'Content-Type':'application/json',
    'Cookie':'Hm_lvt_b88419cfd6f98a39770a416b70174fbc=1611419226;Hm_lpvt_b88419cfd6f98a39770a416b70174fbc=1611419226',
    'Host':'www.ahtba.org.cn',
    'Origin':'http://www.ahtba.org.cn',
    'Referer':'http://www.ahtba.org.cn/site/trade/affiche/gotoTradeList?tradeType=01&classify=A&affiche=A04',
    'User-Agent':'Mozilla/5.0(Linux;Android6.0;Nexus5Build/MRA58N)AppleWebKit/537.36(KHTML,likeGecko)Chrome/87.0.4280.88MobileSafari/537.36',
    'X-Requested-With':'XMLHttpRequest'
    }
    session.headers=headers
    res = session.post(url=url_2,data=json.dumps(data))
    html = etree.HTML(res.text)
    res_list = html.xpath('//div[@class="titBox"]')
    for item in res_list:
        link = item.xpath('div/a/@href')[0]
        text = item.xpath('div/a/text()')[0]
        date = item.xpath('div[@class="fr nums"]/text()')[0]
        try:
            print(date, link, text)
        except:
            pass