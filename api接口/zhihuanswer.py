# coding=utf-8
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import json
import re
REG = re.compile('<[^>]*>')

class  ZhihuSpider(object):
    def __init__(self):
        self.url ="https://www.zhihu.com/api/v4/questions/406777225/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=5&platform=desktop&sort_by=default"
        self.header = {"User-Agent":UserAgent().random}
        self.num =0

    def get_page(self):
        file = open('answers.md','w')
        next_url = [self.url]
        print(next_url)
        count = 0
        for url in next_url:
            proxy = requests.get("http://127.0.0.1:5010/get_all/").json()
            proxies = {"http": "http://{}".format(proxy)}
            html = requests.get(url, headers=self.header,proxies=proxies)
            html.encoding = html.apparent_encoding
            soup = BeautifulSoup(html.text, "lxml")
            content = str(soup.p).split("<p>")[1].split("</p>")[0]
            c = json.loads(content)
            answers = [self.extract_answer(item["content"]) for item in c["data"] if self.extract_answer(item["content"]) != ""]

            try:
                for answer in answers:
                    count+=1
                    print(count,answer)
                    file.write('answer'+str(count)+":")
                    file.write(answer+'\n\n')
            except:
                pass
            
            next_url.append(c["paging"]["next"])
            if c["paging"]["is_end"]:
                break
        file.close()

    def extract_answer(self,s):
        temp_list = REG.sub("", s).replace("\n", "").replace(" ", "")
        return temp_list

if __name__=="__main__":
    spider =ZhihuSpider()
    spider.get_page()
