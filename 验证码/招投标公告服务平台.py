import random
from io import BytesIO
import numpy as np
import requests
from PIL import Image
from lxml import etree

# 获取缺口位置
def get_point(bg_url, full_url, index):
    img_data1 = requests.get(url=bg_url).content
    img_data2 = requests.get(url=full_url).content
    with open('1.png','wb') as f:
        f.write(img_data1)
    with open('2.png', 'wb') as f:
        f.write(img_data2)
    img1 = Image.open(BytesIO(img_data1))
    img2 = Image.open(BytesIO(img_data2))

    def is_similar_color(x_pixel, y_pixel):
        # 颜色对比
        if sum(np.abs(np.array(x_pixel) - np.array(y_pixel))) >= 200:
            return True

    # 计算距离
    def get_offset_distance(cut_image, full_image, index):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if is_similar_color(cpx, fpx):
                    img = full_image.crop((x, y, x + 45, y + 40))
                    # 保存一下计算出来位置图片，看看是不是缺口部分
                    img.save("position.png")
                    return [{"x": x - 12, "y": random.randint(-3, 3)}] # 寸在偏移值

    return get_offset_distance(img1, img2, index)



if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    session = requests.session()
    respose = session.post(url='https://bulletin.cebpubservice.com/captcha/captcha/captchaImage')
    js_data = respose.json()
    url1 = 'https://bulletin.cebpubservice.com/captcha/captcha/image/'+js_data['bigImgName']
    url2 = 'https://bulletin.cebpubservice.com/captcha/captcha/image/'+js_data['sourceImgName']
    dataToken = js_data['dataToken']
    point = str(get_point(url1,url2,0)[0]['x'])
    print(dataToken,point)
    data = {
        'dataToken': dataToken,
        'point': point
    }
    response = session.post('https://bulletin.cebpubservice.com/captcha/captcha/checkCaptcha', headers=headers, data=data)
    token = response.json()['data']
    print(response.text)

    for i in range (1,500):
        try:
            params = (
                ('searchDate', '2021-21'),
                ('dates', '0'),
                ('categoryId', '88'),
                ('industryName', ''),
                ('area', ''),
                ('status', ''),
                ('publishMedia', ''),
                ('sourceInfo', ''),
                ('showStatus', ''),
                ('word', ''),
                ('page', i),
                ('token', token),
            )

            response = session.get('https://bulletin.cebpubservice.com/xxfbcmses/search/bulletin.html', headers=headers, params=params)
            selector = etree.HTML(response.text)
            try:
                titles = selector.xpath('/html/body/table//tr/td[1]/a')
                for title in titles:
                    print(title.text.strip())
            except:
                pass
        except:
            pass