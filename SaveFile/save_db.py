
# -*- encoding = utf-8 -*-
import requests
from lxml import etree
import csv
import json
import pymysql
import pymongo


class Spider(object):
    def __init__(self):
        self.url = "https://www.zhihu.com/hot"
        self.header ={
            'cookie': '_zap=fcb52d30-b35f-4ffb-9b3d-8367ef23573b; _xsrf=4OJ3efFKGn5VGW9AYOqbUysKvd9Z0kb0; d_c0="AJBVa1iCfhKPTnYh0DfWvT-BmsTLL6ycwlU=|1610507531"; __snaker__id=9aVgx3DZ3otve5TC; _9755xjdesxxd_=32; YD00517437729195%3AWM_NI=7cC%2FJ1WzVVejzmf3GtwyuN2%2BKYQUPs8TE3tvAbG1ZNaLWLR0njJWdNs8IvCzkabu7ipt9LM2jqaMCm0r67%2FE2wJZF7CTHGqhtbhfOSr7QMXz61HlxNft%2B22b8hKchdHlWEw%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eea6b673aca8e1d0d83b91ef8fb3d14b979a9babf16f89ea9d9ab87294aea88dc22af0fea7c3b92af5bd8dd0c93b95a69ab7e862bab3aad4c680b5a7bbafb12189879fb6d379fc8c8bd4f77e83be89d2d946a39499add13caeb686b8e746b1e88797c272a9bfae96b663b4acf7add03aaaafafaec267f4aefad8ae4ff2a986bbc53d818c88a8f464b8bea887ce59b2e99faedb72f6ef888dfb46a6ace5d3b16afcb88584eb708cb499a6f637e2a3; YD00517437729195%3AWM_TID=Qdr%2FBCbOSjlARVABERY7OP%2FHj5yKrg0H; captcha_session_v2="2|1:0|10:1610509100|18:captcha_session_v2|28:YnZ2Nm1iNjRmbzZucWhsNnQ0cWc=|551c5a71fdc7f9903526a10caa3df898d7c67f010b862bfc18484c0906932048"; gdxidpyhxdE=OJtLZLJyCtMqtIwEXzsOvDmEwEqyK7s5NSKc%2FeLzgn5SMYPa%2BLWLtPLzBdsvmnq3ftXqXuTsb3HbW2r6Yi5pNO2zlMuIB9wBqxSIx16qYlP7JzUxzbUVqhVqfQV2SItnx6h55O80n3rRkYdBQ%2FOn53hZBXC9Y0LEG%2BOe7%2BMXEqBZGnQJ%3A1610510000504; r_cap_id="NjEzYjViYTIxMDZmNDhmMzliM2NlYWEyNDU1ZTMyMGE=|1610509103|5c9eb7b1b777d1d3c3a677a26b5084aad2f4cf89"; cap_id="YmY0NWIwMmQ3NTY1NGZkY2FkZTAyNzJkN2YyMzQ4MWQ=|1610509103|16ecc04944fd0ffbe19c46162ba3c8522f23f9da"; l_cap_id="NTBjNTMxMTA0MDM1NGFjYjlhMDgzMTllM2Q2OTZkZDc=|1610509103|bfa30ecb3bd703cc5faf577dbb088bb78ef49cf5"; z_c0=Mi4xbDY4cERRQUFBQUFBa0ZWcldJSi1FaGNBQUFCaEFsVk5Pcm5yWUFBTE5ZZW9adFZxYmdCU1NkN0lSZWZJNVAxSXBR|1610509114|fb25fcd0d292339a3410541541d9d0a7bc8780ca; q_c1=a0fee322eaf34cd089ca4302c4680827|1610509978000|1610509978000; tshl=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1610528502,1610537785,1610546552,1610591921; tst=h; SESSIONID=O2MI7cPul6iSBjm3ioWrrBdn1frsAfDWkybLSlwNHYs; JOID=Wl4RBUjWYL7c5EVlHdjFpfO6yR4Dl1DxkNgoN2qxWNWNoyQGLAuKRo3hSWUaPLhOCry41k8jdmEAtWvy4oJAqfM=; osd=VF0RC0zYY77S4EtmHdbBq_C6xxoNlFD_lNYrN2S1VtaNrSAILwuEQoPiSWseMrtOBLi21U8tcm8DtWX27IFAp_c=; KLBRSID=fe0fceb358d671fa6cc33898c8c48b48|1610607657|1610607310',
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36"
        }
        self.infolist=[]

    def  get_page(self):
        res = requests .get(url=self.url,headers=self.header)
        if(res.status_code==200):
            html = etree.HTML(res.content.decode('utf-8'))
            newsList= html.xpath('//div[@class="css-at0ikb"]/a')
            for item in newsList:
                try:
                    link = item.xpath('@href')[0]
                    rank = item.xpath('./div[@class="css-t21nix"]/div/text()')[0]
                    title = item.xpath('./div[@class="css-1mx3lj4"]/h1[@class="css-3yucnr"]/text()')[0]
                    self.infolist.append((rank,link,title))
                except:
                    pass

    def save_mysqldb(self):
        db = pymysql.connect(host='localhost', user='root', password='mk47908493', port=3306, db='spider')
        cursor = db.cursor()
        sql = 'INSERT INTO zhihuhotnews(rank, links, title) values(%s, %s, %s)'
        for item in self.infolist:
            rank = item[0]
            link = item[1]
            title = item[2]
            try:
                cursor.execute(sql, (rank,link, title))
                db.commit()
            except:
                db.rollback()
        db.close()

    def save_mongodb(self):
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client.Spider
        collection = db.zhihuHotnews
        list = []
        for item in self.infolist:
            rank = item[0]
            link = item[1]
            title = item[2]
            news = {}
            news['rank'] = rank
            news['link'] = link
            news['title'] = title
            list.append(news)
            # one by one insert
            # result = collection.insert_one(news)
        # all the news insert into mongodb
        result = collection.insert_many(list)
        print(result)

    def main(self):
        self.get_page()
        # self.save_mysqldb()
        self.save_mongodb()



if __name__ == '__main__':
    newsSpider = Spider()
    newsSpider.main()
