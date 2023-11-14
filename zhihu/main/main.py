# coding=utf-8
import os
import re
import json
import requests
from utils import js_81
from utils import get_x_zse_96, get_timestamp, extract_answer, following_x_zse_96, vote_xzst_96

from login.load_cookies import cookies_dict
# 以下两个忘了可用不可用了
REG = re.compile('<[^>]*>')
all_data = {}


class ZhiUserClass:
    def __init__(self, url_token) -> None:
        self.domain = "https://www.zhihu.com"
        self.cookie_dc0 = cookies_dict["d_c0"]
        self.url_token = url_token

        self.cookies = cookies_dict

    # 获取知乎对象的活动信息
    def user_activities(self):

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
                "x-zse-93": "101_3_3.0",
                'x-zse-96': x_96
            }
            req_answer_url = self.domain + anwsers_url

            responses = requests.get(
                url=req_answer_url, headers=headers, cookies=self.cookies)
            resp_code = responses.status_code
            if resp_code == 200:
                print('状态码'+str(resp_code))
            else:
                break
            print(responses.json())
            res_answer_data = self.process_user_activity(
                responses.json(), res_answer_data)

            self.save_file(res_answer_data, "data/activities.json")

    def process_user_activity(self, data, all_data=None):

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
    def user_answers(self):
        res_data = {}
        pageSize = 1  # 从第一页开始爬取
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
                "x-zse-93": "101_3_3.0",
                'x-zse-96': x_96
            }
            req_answer_url = self.domain + url
            responses = requests.get(
                url=req_answer_url, headers=headers, cookies=self.cookies)
            resp_code = responses.status_code
            if resp_code == 200:
                print('状态码'+str(resp_code))
            else:
                break
            data_res = responses.json()
            res_data = self.process_answers(
                data_res, res_data)
            total_num = data_res["paging"]["totals"]
            if (offset > total_num):
                break
            pageSize += 1
        self.save_file(res_data, "data/person_answer.json")

    def process_answers(self, data, all_data=None):
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

    # 获取用户的文章
    def user_acticles(self, url_token=None):
        if url_token is None:
            url_token = self.url_token

        uh = f"/api/v4/members/{url_token}/articles?include=data%5B*%5D.comment_count%2Csuggest_edit%2Cis_normal%2Cthumbnail_extra_info%2Cthumbnail%2Ccan_comment%2Ccomment_permission%2Cadmin_closed_comment%2Ccontent%2Cvoteup_count%2Ccreated%2Cupdated%2Cupvoted_followees%2Cvoting%2Creview_info%2Creaction_instruction%2Cis_labeled%2Clabel_info%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B*%5D.author.vip_info%3B&offset=8&limit=12&sort_by=created"

        x_96 = get_x_zse_96(uh, self.cookie_dc0)
        headers = {
            'accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'X-Requested-With': 'fetch',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            "x-zse-93": "101_3_3.0",
            'x-zse-96': x_96
        }
        url = "https://www.zhihu.com" + uh
        response = requests.get(url=url, headers=headers, cookies=self.cookies)
        print(response.json())

    #  获取用户的专栏信息
    def user_columns(self, url_token=None, save_flag=False):

        url_token = "72-31-98-7"
        url_token = "haku-61"
        uh = f"/api/v4/members/{url_token}/column-contributions?include=data%5B*%5D.column.intro%2Cfollowers%2Carticles_count%2Cvoteup_count%2Citems_count&offset=0&limit=20"

        x_96 = get_x_zse_96(uh, self.cookie_dc0)
        headers = {
            'accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'X-Requested-With': 'fetch',
            # 'Referer': 'https://www.zhihu.com/people/'+url_token+'/activities?page='+str(offset),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            "cookie": 'd_c0="APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843"; _xsrf=HWUgSh20t0DqcQLELvW9aiBDUF9b33tF; q_c1=6b8c51f29aec40b3b5de4a5680882bf3|1645958464000|1645958464000; _zap=b0db2c52-aac3-45a9-a4b5-63fc4e67e0a7; z_c0=2|1:0|10:1697629107|4:z_c0|80:MS4xTF91WkNBQUFBQUFtQUFBQVlBSlZUYXVVRjJZaWVpSXRndFd6RWdCUmwyY2VPdUh1M0djcnZRPT0=|3d38eb60e492abff77f7753d24cb396b164247ad6275aead6368921d317f57af; tst=r; SESSIONID=nBWT56da7Tfbt9dMoNPWtyCxaWHtbdSNAKJ9HiQFaPI; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1698741524|1698739803',
            "x-zse-93": "101_3_3.0",
            'x-zse-96': x_96
        }

        url = "https://www.zhihu.com" + uh

        response = requests.get(url=url, headers=headers)
        res = response.json()["paging"]["totals"]

        # 获取专栏信息
        column_all_data = []
        if res > 0:
            for item in response.json()["data"]: \

                infos = item["column"]
                del infos["author"]
                infos["contributions_count"] = item["contributions_count"]
                column_all_data.append(infos)

        if save_flag is True:
            for item in column_all_data:
                total_num = item["contributions_count"]
                base_url = item["url"]
                print(base_url)
                offset = 0

                while offset < total_num:
                    full_url = base_url + f"/items?limit=10&offset={offset}"
                    uh = full_url.replace("http://www.zhihu.com", "")
                    x_96 = get_x_zse_96(uh, self.cookie_dc0)
                    headers = {
                        'accept': '*/*',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                        'X-Requested-With': 'fetch',
                        # 'Referer': 'https://www.zhihu.com/people/'+url_token+'/activities?page='+str(offset),
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                        "cookie": 'd_c0="APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843"; _xsrf=HWUgSh20t0DqcQLELvW9aiBDUF9b33tF; q_c1=6b8c51f29aec40b3b5de4a5680882bf3|1645958464000|1645958464000; _zap=b0db2c52-aac3-45a9-a4b5-63fc4e67e0a7; z_c0=2|1:0|10:1697629107|4:z_c0|80:MS4xTF91WkNBQUFBQUFtQUFBQVlBSlZUYXVVRjJZaWVpSXRndFd6RWdCUmwyY2VPdUh1M0djcnZRPT0=|3d38eb60e492abff77f7753d24cb396b164247ad6275aead6368921d317f57af; tst=r; SESSIONID=nBWT56da7Tfbt9dMoNPWtyCxaWHtbdSNAKJ9HiQFaPI; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1698741524|1698739803',
                        "x-zse-93": "101_3_3.0",
                        'x-zse-96': x_96
                    }

                    response = requests.get(url=full_url, headers=headers)

                    # 后面可以选择存储操作

        return column_all_data

    # 获取知乎的用户的关注者或者关注的人
    def user_person_relation(self, relation_type="followees"):
        """
            The relation_type value: followees or followers
        """
        all_data = {}  # the savaed results
        page_N = 1
        while True:

            offset = (page_N-1) * 20
            uh = "/api/v4/members/"+self.url_token + "/" + relation_type +\
                "?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=" + \
                str(offset)+"&limit=20"

            x_96 = get_x_zse_96(uh, self.cookie_dc0)

            url = "https://www.zhihu.com" + uh

            headers = {
                'accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'X-Requested-With': 'fetch',
                'Referer': f'https://www.zhihu.com/people/'+self.url_token+'/{relation_type}?page='+str(page_N),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                "cookie": 'd_c0="APDcLdkxgxOPTiJpWgSNn6GikHyNF0VMK3E=|1628001843"; _xsrf=HWUgSh20t0DqcQLELvW9aiBDUF9b33tF; q_c1=6b8c51f29aec40b3b5de4a5680882bf3|1645958464000|1645958464000; _zap=b0db2c52-aac3-45a9-a4b5-63fc4e67e0a7; z_c0=2|1:0|10:1697629107|4:z_c0|80:MS4xTF91WkNBQUFBQUFtQUFBQVlBSlZUYXVVRjJZaWVpSXRndFd6RWdCUmwyY2VPdUh1M0djcnZRPT0=|3d38eb60e492abff77f7753d24cb396b164247ad6275aead6368921d317f57af; tst=r; SESSIONID=nBWT56da7Tfbt9dMoNPWtyCxaWHtbdSNAKJ9HiQFaPI; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1698741524|1698739803',
                "x-zse-93": "101_3_3.0",
                'x-zse-96': x_96
            }
            responses = requests.get(url=url, headers=headers)
            resp_code = responses.status_code
            if resp_code == 200:
                print('状态码'+str(resp_code))

            print(responses.json)
        #     for item in responses.json()["data"]:
        #         person_info = {}
        #         person_info["username"] = item["name"]
        #         person_info["url"] = item["url"]
        #         person_info["url_token"] = item["url_token"]
        #         person_info["follower_count"] = item["follower_count"]
        #         person_info["articles_count"] = item["articles_count"]
        #         person_info["answer_count"] = item["answer_count"]
        #         person_info["gender"] = item["gender"]
        #         person_info["answer_count"] = item["answer_count"]
        #         person_info["answer_count"] = item["answer_count"]
        #         person_info["answer_count"] = item["answer_count"]
        #         person_info["answer_count"] = item["answer_count"]
        #         person_info["answer_count"] = item["answer_count"]
        #         person_info["answer_count"] = item["answer_count"]
        #         person_info["user_type"] = item["user_type"]
        #         all_data[item["id"]] = person_info
        #     # 判断是不是最后的一页数据
        #     if responses.json()["paging"]["is_end"] is True:
        #         break
        #     else :
        #         page_N+=1

        # print(len(all_data.keys()))
        # self.save_file(all_data,f"data/{self.url_token}_{relation_type}.json")

    def user_followees(self):

        followee_list = []
        page_N = 1
        all_data = {}
        while True:
            offset = (page_N-1) * 20
            uh = "/api/v4/members/"+self.url_token + \
                "/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=" + \
                str(offset)+"&limit=20"

            x_96 = get_x_zse_96(uh, self.cookie_dc0)

            url = "https://www.zhihu.com" + uh
            headers = {
                'accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'X-Requested-With': 'fetch',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                "x-zse-93": "101_3_3.0",
                'x-zse-96': x_96
            }
            responses = requests.get(
                url=url, headers=headers, cookies=self.cookies)
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

                followee_list.append(item["url_token"])
                all_data[item["url_token"]] = person_info
            if responses.json()["paging"]["is_end"]:
                break
            else:
                page_N += 1

        self.save_file(all_data, f"data/{self.url_token}_followees.json")
        return followee_list

    def user_followers(self):

        page_N = 1

        all_data = {}

        while True:
            offset = (page_N-1) * 20

            uh = "/api/v4/members/"+self.url_token + \
                "/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=" + \
                str(offset)+"&limit=20"

            x_96 = get_x_zse_96(uh, self.cookie_dc0)

            url = "https://www.zhihu.com" + uh

            headers = {
                'accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'X-Requested-With': 'fetch',
                'Referer': 'https://www.zhihu.com/people/'+self.url_token+'/followees?page='+str(page_N),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                "x-zse-93": "101_3_3.0",
                'x-zse-96': x_96
            }
            responses = requests.get(
                url=url, headers=headers, cookies=self.cookies)
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
            if responses.json()["paging"]["is_end"] is True:
                break
            else:
                page_N += 1

        self.save_file(all_data, "data/following.json")

    #  关注操作必须需要x_zst_81参数一直变量输入到x_zst_96参数中作为变量从而进行获取最终的x_zst_96参数，然后才会起作用
    def get_followee(self, url_token):

        cookies_dc0 = "AADV-s-OqxePTnGj_8cpRvuHsELYgBuvAdw=|1699430044"

        url = f"https://www.zhihu.com/api/v4/members/{url_token}/followers"

        uh = url.replace("https://www.zhihu.com", "")
        x_96 = following_x_zse_96(uh, cookies_dc0, js_81)
        headers = {
            "authority": "www.zhihu.com",
            "accept": "*/*",
            "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
            "cache-control": "no-cache",
            "origin": "https://www.zhihu.com",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "x-requested-with": "fetch",
            "x-zse-93": "101_3_3.0",
            "x-zse-96": x_96,
            "x-zst-81": js_81
        }
        cookies = {
            "d_c0":  "AADV-s-OqxePTnGj_8cpRvuHsELYgBuvAdw=|1699430044",
            "z_c0": "2|1:0|10:1699430203|4:z_c0|92:Mi4xT1hSalB3QUFBQUFBQU5YNno0NnJGeGNBQUFCZ0FsVk5PNDA0WmdCanRsaEJ6OGhsUXdmT2V4MUo3UU9ZdUpxRmlR|e940dff86cae26559b94b507aa4459630d9c9bd9074d2a25613c4525018966cc",
        }

        response = requests.post(url, headers=headers, cookies=cookies)
        print(response.json())

    def del_followee(self, url_token):

        cookies_dc0 = "AADV-s-OqxePTnGj_8cpRvuHsELYgBuvAdw=|1699430044"

        url = f"https://www.zhihu.com/api/v4/members/{url_token}/followers"

        uh = url.replace("https://www.zhihu.com", "")

        x_96 = following_x_zse_96(uh, cookies_dc0, js_81)

        headers = {
            "authority": "www.zhihu.com",
            "accept": "*/*",
            "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
            "cache-control": "no-cache",
            "origin": "https://www.zhihu.com",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "x-requested-with": "fetch",
            "x-zse-93": "101_3_3.0",
            "x-zse-96": x_96,
            "x-zst-81": js_81
        }
        cookies = {
            "d_c0": "AADV-s-OqxePTnGj_8cpRvuHsELYgBuvAdw=|1699430044",
            "z_c0": "2|1:0|10:1699430203|4:z_c0|92:Mi4xT1hSalB3QUFBQUFBQU5YNno0NnJGeGNBQUFCZ0FsVk5PNDA0WmdCanRsaEJ6OGhsUXdmT2V4MUo3UU9ZdUpxRmlR|e940dff86cae26559b94b507aa4459630d9c9bd9074d2a25613c4525018966cc",
        }

        response = requests.delete(url, headers=headers, cookies=cookies)
        print(response.json())
    # 保存信息

    def save_file(self, data, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
            file.close()

    def vote_likes(self, answers_id=None, like_type=None):
        """
            like_type: up、down or neutral 
        """

        url = f"https://www.zhihu.com/api/v4/answers/{answers_id}/voters"
        data = {
            "type": f'{like_type}'
        }
        uh = url.replace("https://www.zhihu.com", "")
        params_data = json.dumps(data).replace(' ', '')
        x_96 = vote_xzst_96(uh, self.cookie_dc0, params_data, js_81)
        headers = {
            "authority": "www.zhihu.com",
            "accept": "*/*",
            "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
            "content-type": "application/json",
            "origin": "https://www.zhihu.com",
            # "referer": "https://www.zhihu.com/question/630017159",
            "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "x-requested-with": "fetch",
            "x-zse-93": "101_3_3.0",
            "x-zse-96": x_96,
            "x-zst-81": js_81
        }

        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=headers,
                                 cookies=self.cookies, data=data)
        print(response.json())
        print(response)

    def get_rootcomments(self, answers_id=None):

        url = "https://www.zhihu.com/api/v4/comment_v5/answers/3288053222/root_comment?order_by=score&limit=20&offset="
        while True:
            uh = url.replace("https://www.zhihu.com", "")

            x_96 = get_x_zse_96(uh, self.cookie_dc0)

            headers = {
                "authority": "www.zhihu.com",
                "accept": "*/*",
                "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
                "referer": "https://www.zhihu.com/question/630017159",
                "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                "x-requested-with": "fetch",
                "x-zse-93": "101_3_3.0",
                "x-zse-96": x_96
            }
            response = requests.get(url, headers=headers, cookies=self.cookies)
            try:
                data = response.json()
                for item in data["data"]:
                    print(item["id"], item["content"])
                if data["paging"]["is_end"]:
                    break
                else:
                    url = data["paging"]["next"]
            except:
                break

    def get_childcomments(self, comment_id=None):

        url = f"https://www.zhihu.com/api/v4/comment_v5/comment/{comment_id}/child_comment?order_by=ts&limit=20&offset="
        while True:
            uh = url.replace("https://www.zhihu.com", "")
            x_96 = get_x_zse_96(uh, self.cookie_dc0)
            headers = {
                "authority": "www.zhihu.com",
                "accept": "*/*",
                "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
                "referer": "https://www.zhihu.com/question/630017159",
                "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                "x-requested-with": "fetch",
                "x-zse-93": "101_3_3.0",
                "x-zse-96": x_96
            }
            response = requests.get(url, headers=headers, cookies=self.cookies)
            try:
                data = response.json()
                for item in data["data"]:
                    print(item["content"])
                if data["paging"]["is_end"]:
                    break
                else:
                    url = data["paging"]["next"]
            except:
                break

    def get_uerinfo(self, user_id=None):

        url = f"https://www.zhihu.com/api/v4/members/{user_id}?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics"
        uh = url.replace("https://www.zhihu.com", "")
        j_96_params = get_x_zse_96(uh, self.cookie_dc0)
        headers = {
            "authority": "www.zhihu.com",
            "accept": "*/*",
            "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
            "referer": "https://www.zhihu.com/question/542991276/answer/3269914167",
            "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "x-requested-with": "fetch",
            "x-zse-93": "101_3_3.0",
            "x-zse-96": j_96_params,
        }
        response = requests.get(url, headers=headers, cookies=self.cookies)
        try:
            data = response.json()
            print(data["ip_info"])
        except:
            print("出现错误！")


# if __name__ == "__main__":

#     url_token = 'todo-31-69'
#     target_url = "72-31-98-7"
#     zhihu = ZhiUserClass(url_token=url_token)
#     zhihu.user_answers()
#     zhihu.user_acticles()

#     zhihu.user_followers()
#     followee_list = zhihu.user_followees()

#     zhihu.get_uerinfo(target_url)
#     zhihu.user_answers()

#     zhihu.user_activities()
