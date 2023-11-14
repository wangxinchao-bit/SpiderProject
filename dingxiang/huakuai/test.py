import requests
from PIL import Image

import execjs 
def get_png():

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Origin": "https://www.dingxiang-inc.com",
        "Referer": "https://www.dingxiang-inc.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://cap.dingxiang-inc.com/api/a"
    params = {
        "w": "380",
        "h": "165",
        "s": "50",
        "ak": "99de95ad1f23597c23b3558d932ded3c",
        "c": "",
        "jsv": "6.0.0",
        "aid": "dx-1699777844863-63521771-3",
        "wp": "1",
        "de": "0",
        "uid": "",
        "lf": "0",
        "tpc": "",
        "cid": "43487257",
        "_r": "0.2335381885043104"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    img_background = data["p1"]
    img_front = data["p2"]

    background_url = "https://static.dingxiang-inc.com/picture/"+ img_background
    response = requests.get(url=background_url)
    print(url)
    with open("images/background.webp","wb") as file:
        file.write(response.content)

    front_url = "https://static.dingxiang-inc.com/picture/"+ img_front
    response = requests.get(url=front_url)
    with open("images/front.webp","wb") as file:
        file.write(response.content)
    
    return background_url

def recover_img(background_url):

    filenamme = background_url.split("/")[-1].split(".")[0]
    with open('pos.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
        js_text = execjs.compile(js_code)
    arr = js_text.call('encrypy',filenamme)

    _img = Image.open("images/background.webp")

    new_img = Image.new('RGB', (400, 200))  # 宽400 高200
    for index in range(len(arr)):
        c = arr[index] * 12
        # 从背景图中扣出相应的小图
        l = _img.crop((c, 0, c + 12,200))  # 图片剪切crop(x,y,x1,y1) 四个坐标
        # 将扣出的小图 还原到正确的位置
        new_x = index * 12
        new_img.paste(l, (new_x, 0))
    new_img.paste(_img.crop((384, 0, 400,200)),(384,0))  # 最后的边框 32*12=384
    new_img.save("background.jpg")


if __name__=="__main__":
    background_url = get_png()
    recover_img(background_url)


