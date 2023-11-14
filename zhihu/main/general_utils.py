# coding=utf-8
import os
import re
import json
import requests
from datetime import datetime

from utils import js_81
from utils import get_x_zse_96, get_timestamp, extract_answer,following_x_zse_96,vote_xzst_96


from login.load_cookies import cookies_dict

class ZhiGeneral:
    def __init__(self) -> None:
        self.domain = "https://www.zhihu.com"
        self.cookie_dc0 = cookies_dict["d_c0"]

    def get_hotnew(self):
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true"
        data = requests.get(url=url).json()
        all_hotnews = {}
        count = 0
        try:
            for item in data["data"]:
                item = item["target"]
                new_info = {}
                new_info["title"] = item["title_area"]["text"]
                new_info["hotspots"] = item["metrics_area"]["text"]
                new_info["link"] = item["link"]["url"]
                new_info["image_url"] = item["image_area"]["url"]
                all_hotnews[str(count)] = new_info
                count += 1
        except:
            for item in data["data"]:
                new_info = {}
                new_info["title"] = item["target"]["title"]
                new_info["url"] = item["target"]["url"]
                all_hotnews[str(count)] = new_info
                count += 1
        else:
            pass
        date = datetime.now()
        file_name = str(date.month) + "_" + str(date.day)
        with open(f"{file_name}.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(all_hotnews, ensure_ascii=False))

    def get_questionAnswers(self,question_id):

        url = f"https://www.zhihu.com/api/v4/questions/{question_id}/feeds?cursor=&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=5&order=default&platform=desktop"

        question_dir = f"QA_{question_id}/"
        if not os.path.exists(question_dir):
            os.mkdir(question_dir)
        # #  "存储为csv文件信息"
        # csv_file = open('data_res.csv', 'w', newline='', encoding="utf-8")
        # writer = csv.writer(csv_file)
        # writer.writerow("answers")
        # count = 0
        while True:
            answers_list = requests.get(url=url).json()
            for item in answers_list["data"]:
                infos = item["target"]
                timestamp = infos["updated_time"]
                answername = infos["author"]["name"]
                content = infos["content"]
                # timestamp = utc_datetime = datetime.utcfromtimestamp(timestamp)
                res_content = self.extract_content(content)
                filenames = os.path.join(question_dir,f"{timestamp}_{answername}.md")
                with open(filenames,"w",encoding="utf-8") as file:
                    file.write(res_content)
                    file.close()
            break
            if answers_list["paging"]["is_end"] :
                break
            else:
                url = answers_list["paging"]["next"]

    
    def extract_content(self,html_content):
                
        # Define a regular expression pattern to match both text within <p> tags and image src attributes within <img> tags
        combined_pattern = re.compile(r'(<p [^>]*>.*?</p>|<img[^>]*src="([^"]+)".*?>)', re.DOTALL)

        # Use findall to get all matches
        matches = re.findall(combined_pattern, html_content)

        # Initialize variables to store the final result
        result = []
        current_text = ""
        current_images = []

        # Iterate through matches
        for match in matches:
            if match[0].startswith('<p'):
                # If the match is a paragraph, store the previous text and images, then reset
                if current_text or current_images:

                    result.append({'text_content': current_text, 'image_links': current_images})
                    current_text = ""
                    current_images = []
                current_text += match[0]
            elif match[0].startswith('<img'):
                # If the match is an image, add the image link to the current_images list
                current_images.append(match[1])

        # Store the last text and images
        if current_text or current_images:
            result.append({'text_content': current_text, 'image_links': current_images})

        res =""
        # Print the result
        for entry in result:
            res +=entry['text_content']
            for img_link in entry['image_links']:
                res += f"![{img_link}]({img_link})" + " "

        return res

    def extract_answer(self, s):
        data = s.replace("\\", "")
        images_list = re.findall('img src="(http.*?)"', data, re.S)
        temp_list = REG.sub("", s).replace("\n", "").replace(" ", "")
        return temp_list, images_list


if __name__ == "__main__":
    zhihu = ZhiGeneral()
    zhihu.get_hotnew()
    zhihu.get_questionAnswers(630059744)