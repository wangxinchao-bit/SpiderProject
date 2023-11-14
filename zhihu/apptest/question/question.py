# coding=utf-8
import requests
import json
import re
import csv
import random
import time
import os
import base64
REG = re.compile('<[^>]*>')


class ZhihuSpider(object):
    def __init__(self, question_id):
        self.url = f"https://www.zhihu.com/api/v4/questions/{question_id}/feeds?cursor=&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop&session_id="
        # 图像的存储文件夹
        img_dir = "./images"
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)

    def get_page(self):
        #  "存储为csv文件信息"
        csv_file = open('data_res.csv', 'w', newline='', encoding="utf-8")
        writer = csv.writer(csv_file)
        writer.writerow("answers")
    
        count = 0
        while True:
            answers_list = requests.get(self.url).json()
            for item in answers_list["data"]:
                answer_content = item["target"]["content"]
                extract_res = self.extract_answer(answer_content)
                data_info = extract_res[0]
                img_count = 0
                csv_row_info = [count, data_info]
                try:
                    for img_url in extract_res[1]:
                        img_count += 1
                        with open(f'images/{count}_{img_count}.png', 'wb') as f:
                            img_data = requests.get(img_url).content
                            f.write(img_data)
                            csv_row_info.append(img_url)
                except:
                    pass
                writer.writerow(csv_row_info)
                count += 1
            try:
                self.url = answers_list["paging"]["next"]
                pause_falg = answers_list["paging"]["is_end"]
            except:
                break
            if pause_falg:
                break
            print(count)
            time.sleep(random.randint(1, 3))
        csv_file.close()

    def extract_answer(self, s):
        data = s.replace("\\", "")
        images_list = re.findall('img src="(http.*?)"', data, re.S)
        temp_list = REG.sub("", s).replace("\n", "").replace(" ", "")
        return temp_list, images_list

if __name__ == "__main__":
    spider = ZhihuSpider(629993688)
    spider.get_page()
