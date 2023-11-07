

# coding=utf-8

import os
import re
import time
import random
import json
import requests
import hashlib
import base64
import subprocess
from tqdm import tqdm

from utils import get_x_zse_96, get_timestamp, extract_answer

all_data = {}


def user_followees(page_N):

    url_token = 'quantkoala'

    offset = (page_N-1) * 20

    cookie_dc0 = "\"APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843\""
    uh = "/api/v4/members/"+url_token + \
        "/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=" + \
        str(offset)+"&limit=20"

    x_96 = get_x_zse_96(uh, cookie_dc0)

    url = "https://www.zhihu.com/api/v4/members/"+url_token + \
        "/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=" + \
        str(offset)+"&limit=20"

    headers = {
        'accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'X-Requested-With': 'fetch',
        'Referer': 'https://www.zhihu.com/people/'+url_token+'/followees?page='+str(page_N),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        "cookie": 'd_c0="APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843"; _xsrf=HWUgSh20t0DqcQLELvW9aiBDUF9b33tF; q_c1=6b8c51f29aec40b3b5de4a5680882bf3|1645958464000|1645958464000; _zap=b0db2c52-aac3-45a9-a4b5-63fc4e67e0a7; z_c0=2|1:0|10:1697629107|4:z_c0|80:MS4xTF91WkNBQUFBQUFtQUFBQVlBSlZUYXVVRjJZaWVpSXRndFd6RWdCUmwyY2VPdUh1M0djcnZRPT0=|3d38eb60e492abff77f7753d24cb396b164247ad6275aead6368921d317f57af; tst=r; SESSIONID=nBWT56da7Tfbt9dMoNPWtyCxaWHtbdSNAKJ9HiQFaPI; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1698741524|1698739803',
        "x-zse-93": "101_3_3.0",
        'x-zse-96': x_96
    }
    responses = requests.get(url=url, headers=headers)
    resp_code = responses.status_code
    if resp_code == 200:
        print('状态码'+str(resp_code))

    for item in responses.json()["data"]:
        person_info = {}
        person_info["username"] = item["name"]
        person_info["url"] = item["url"]
        person_info["url_token"] = item["url_token"]
        person_info["follower_count"] = item["follower_count"]
        person_info["articles_count"] = item["articles_count"]
        person_info["answer_count"] = item["answer_count"]
        person_info["gender"] = item["gender"]
        person_info["answer_count"] = item["answer_count"]
        person_info["answer_count"] = item["answer_count"]
        person_info["answer_count"] = item["answer_count"]
        person_info["answer_count"] = item["answer_count"]
        person_info["answer_count"] = item["answer_count"]
        person_info["answer_count"] = item["answer_count"]
        person_info["user_type"] = item["user_type"]
        all_data[item["id"]] = person_info


class Zhihu:
    def __init__(self, url_token) -> None:
        self.domain = "https://www.zhihu.com"
        self.cookie_dc0 = "\"APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843\""
        self.url_token = url_token

    # 获取知乎对象的活动信息
    def user_answers(self):

        res_answer_data = {}

        for page_num in range(1, 2):

            anwsers_url = f"/api/v3/moments/{self.url_token}/activities?offset={get_timestamp()}&page_num={page_num}"

            x_96 = get_x_zse_96(anwsers_url, self.cookie_dc0)

            headers = {
                'accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'X-Requested-With': 'fetch',
                'Referer': 'https://www.zhihu.com/people/'+url_token+'/activities?page='+str(page_num),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                "cookie": 'd_c0="APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843"; _xsrf=HWUgSh20t0DqcQLELvW9aiBDUF9b33tF; q_c1=6b8c51f29aec40b3b5de4a5680882bf3|1645958464000|1645958464000; _zap=b0db2c52-aac3-45a9-a4b5-63fc4e67e0a7; z_c0=2|1:0|10:1697629107|4:z_c0|80:MS4xTF91WkNBQUFBQUFtQUFBQVlBSlZUYXVVRjJZaWVpSXRndFd6RWdCUmwyY2VPdUh1M0djcnZRPT0=|3d38eb60e492abff77f7753d24cb396b164247ad6275aead6368921d317f57af; tst=r; SESSIONID=nBWT56da7Tfbt9dMoNPWtyCxaWHtbdSNAKJ9HiQFaPI; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1698741524|1698739803',
                "x-zse-93": "101_3_3.0",
                'x-zse-96': x_96
            }

            req_answer_url = self.domain + anwsers_url

            responses = requests.get(url=req_answer_url, headers=headers)
            resp_code = responses.status_code
            if resp_code == 200:
                print('状态码'+str(resp_code))
            else:
                break
            res_answer_data = self.process_user_answer(
                responses.json(), res_answer_data)

            self.save_file(res_answer_data, "data/answer.json")

    def process_user_answer(self, data, all_data=None):

        if all_data is None:
            all_data = {}

        answer_data = data["data"]
        for answer in answer_data:
            need_answe_info = {}
            id = answer["id"]
            need_answe_info["created_time"] = answer["created_time"]
            need_answe_info["content"] = extract_answer(
                str(answer["target"]["content"]))
            need_answe_info["url"] = answer["target"]["url"]
            try:
                need_answe_info["voteup_count"] = answer["target"]["voteup_count"]
                need_answe_info["thanks_count"] = answer["target"]["thanks_count"]
                need_answe_info["question_title"] = answer["target"]["question"]["url"]
                need_answe_info["question_url"] = answer["target"]["question"]["title"]
            except:
                pass
            need_answe_info["verb"] = answer["verb"]
            all_data[id] = need_answe_info
        return all_data

    # 获取用户的问答文章

    def activaty(self):
        
        res_data ={}
        
        pageSize = 1 # 从第一页开始爬取
        while True:
            offset = (pageSize - 1) * 20
            url = f"/api/v4/members/{self.url_token}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cpaid_info%2Creaction_instruction%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship&offset={offset}&limit=20&sort_by=created"
            x_96 = get_x_zse_96(url, self.cookie_dc0)

            headers = {
                'accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'X-Requested-With': 'fetch',
                'Referer': 'https://www.zhihu.com/people/'+url_token+'/activities?page='+str(offset),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                "cookie": 'd_c0="APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843"; _xsrf=HWUgSh20t0DqcQLELvW9aiBDUF9b33tF; q_c1=6b8c51f29aec40b3b5de4a5680882bf3|1645958464000|1645958464000; _zap=b0db2c52-aac3-45a9-a4b5-63fc4e67e0a7; z_c0=2|1:0|10:1697629107|4:z_c0|80:MS4xTF91WkNBQUFBQUFtQUFBQVlBSlZUYXVVRjJZaWVpSXRndFd6RWdCUmwyY2VPdUh1M0djcnZRPT0=|3d38eb60e492abff77f7753d24cb396b164247ad6275aead6368921d317f57af; tst=r; SESSIONID=nBWT56da7Tfbt9dMoNPWtyCxaWHtbdSNAKJ9HiQFaPI; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1698741524|1698739803',
                "x-zse-93": "101_3_3.0",
                'x-zse-96': x_96
            }

            req_answer_url = self.domain + url

            responses = requests.get(url=req_answer_url, headers=headers)
            resp_code = responses.status_code
            if resp_code == 200:
                print('状态码'+str(resp_code))
            else:
                break
            data_res = responses.json()

            res_data = self.answer_process(
               data_res, res_data)
            total_num = data_res["paging"]["totals"]
            if(offset>total_num):

                break
            
            pageSize += 1

        self.save_file(res_data, "data/person_answer.json")
    
    def answer_process(self, data, all_data=None):
        if all_data is None:
            all_data = {}

        answer_data = data["data"]
        for answer in answer_data:
            need_answe_info = {}
            id = answer["id"]
            need_answe_info["created_time"] = answer["created_time"]
            need_answe_info["content"] = extract_answer(
                str(answer["content"]))
            need_answe_info["url"] = answer["url"]
            try:
                need_answe_info["comment_count"] = answer["comment_count"]
                need_answe_info["voteup_count"] = answer["voteup_count"]
                need_answe_info["question_title"] = answer["question"]["url"]
                need_answe_info["question_url"] = answer["question"]["title"]
            except:
                pass
            all_data[id] = need_answe_info
        return all_data




    def save_file(self, data, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
            file.close()


if __name__ == "__main__":
    #     for i in range(0, 11):
    #         user_followees(i)
    #         import time
    #     with open("res.json", "w") as file:
    #         file.write(json.dumps(all_data, indent=4, ensure_ascii=True))

    url_token = 'quantkoala'
    zhihu = Zhihu(url_token=url_token)
    # zhihu.user_answers()
    zhihu.activaty()
