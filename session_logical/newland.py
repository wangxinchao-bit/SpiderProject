
# -*- coding: utf-8 -*-
import base64,re
import requests
import pytesseract
from PIL import Image
import execjs
import binascii
from lxml import etree
'''
http://www.landchina.com/default.aspx?tabid=226
'''

def str_to_hexStr(string): #字符串转十六进制
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')

'''加密js--字符串转十六进制'''
js_str = '''
    function stringToHex(str) {
        var val = "";
        for (var i = 0; i < str.length; i++) {
            if (val == "") val = str.charCodeAt(i).toString(16); else val += str.charCodeAt(i).toString(16);
        }
        return val;
    }
'''
js = execjs.compile(js_str)


proxies = {'http': 'http://117.185.16.31:80', 'https': 'https://117.185.16.31:80'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

url = 'http://www.landchina.com/default.aspx?tabid=226'
session = requests.session()
yzm_info = session.get(url=url, headers=headers, verify=False)

# print(yzm_info)
# #获取图片base64编码，转为图片
# base64_data = re.compile('src="data:image/bmp;base64,(.*?)"').findall(yzm_info.text)[0]
# ori_image_data = base64.b64decode(base64_data)
# fout = open('yzm.jpg', 'wb')
# fout.write(ori_image_data)
# fout.close()
#
# #识别简单的验证码
# image = Image.open('yzm.jpg')
# result = pytesseract.image_to_string(image).replace(' ','').replace('\n','')
# print('识别的验证码：',result)
#
# #参数加密
# data = js.call('stringToHex',result)
# print('得到的加密参数：',data)
#
# new_url = 'http://www.landchina.com/'+"default.aspx?tabid=226&security_verify_img=" + data
# print('验证码检验地址：',new_url)
# #
#
# #验证码检验
# session.get(new_url, headers=headers, proxies=proxies,verify=False)
#
# #重新请求原网页
response = session.get(url, headers=headers,verify=False)
provinces = re.compile('</td><td class="queryCellBordy">(.*?)</td>').findall(response.text)
print(provinces)
#
#
# 请求下一页地址，__VIEWSTATE和__EVENTVALIDATION参数是类目里固定的参数，TAB_QuerySubmitPagerData是页数

for i in range (1,20):
    i= f'{i}'
    data = {
        '__VIEWSTATE': '/wEPDwUJNjkzNzgyNTU4D2QWAmYPZBYIZg9kFgICAQ9kFgJmDxYCHgNzcmMFN1VzZXIvZGVmYXVsdC9VcGxvYWQvc3lzRnJhbWVJbWcveF90ZHNjdzIwMjBfZmxhc2hfMS5wbmdkAgEPZBYCAgEPFgIeBXN0eWxlBSBCQUNLR1JPVU5ELUNPTE9SOiNmM2Y1Zjc7Q09MT1I6O2QCAg9kFgICAQ9kFgJmD2QWAmYPZBYCZg9kFgRmD2QWAmYPZBYCZg9kFgJmD2QWAmYPZBYCZg8WBB8BBSBDT0xPUjojRDNEM0QzO0JBQ0tHUk9VTkQtQ09MT1I6Ox4HVmlzaWJsZWgWAmYPZBYCAgEPZBYCZg8PFgIeBFRleHRlZGQCAQ9kFgJmD2QWAmYPZBYCZg9kFgRmD2QWAmYPFgQfAQWHAUNPTE9SOiNEM0QzRDM7QkFDS0dST1VORC1DT0xPUjo7QkFDS0dST1VORC1JTUFHRTp1cmwoaHR0cDovL3d3dy5sYW5kY2hpbmEuY29tL1VzZXIvZGVmYXVsdC9VcGxvYWQvc3lzRnJhbWVJbWcveF90ZHNjd19zeV9qaGdnXzAwMC5naWYpOx4GaGVpZ2h0BQEzFgJmD2QWAgIBD2QWAmYPDxYCHwNlZGQCAg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPZBYCZg9kFgRmD2QWAmYPFgQfAQUgQ09MT1I6I0QzRDNEMztCQUNLR1JPVU5ELUNPTE9SOjsfAmgWAmYPZBYCAgEPZBYCZg8PFgIfA2VkZAICD2QWAmYPZBYEZg9kFgJmD2QWAmYPZBYCZg9kFgJmD2QWAmYPZBYCZg8WBB8BBSBDT0xPUjojRDNEM0QzO0JBQ0tHUk9VTkQtQ09MT1I6Ox8CaBYCZg9kFgICAQ9kFgJmDw8WAh8DZWRkAgIPZBYEZg9kFgJmD2QWAmYPZBYCZg9kFgICAQ9kFgJmDxYEHwEFhgFDT0xPUjojMDAwMDAwO0JBQ0tHUk9VTkQtQ09MT1I6O0JBQ0tHUk9VTkQtSU1BR0U6dXJsKGh0dHA6Ly93d3cubGFuZGNoaW5hLmNvbS9Vc2VyL2RlZmF1bHQvVXBsb2FkL3N5c0ZyYW1lSW1nL3hfdGRzY3dfenlfZ2RqaF8wMS5naWYpOx8EBQI0NhYCZg9kFgICAQ9kFgJmDw8WAh8DZWRkAgEPZBYCZg9kFgJmD2QWAmYPZBYCAgEPZBYCZg8WBB8BBSBDT0xPUjojRDNEM0QzO0JBQ0tHUk9VTkQtQ09MT1I6Ox8EZBYCZg9kFgICAQ9kFgJmDw8WAh8DZWRkAgMPZBYCAgMPFgQeCWlubmVyaHRtbAWuEDxwPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+QTpsaW5rIHsgQ09MT1I6IzAwMDAwMDsgVEVYVC1ERUNPUkFUSU9OOk5vbmV9QTp2aXNpdGVkIHsgIENPTE9SOiMwMDAwMDA7IFRFWFQtREVDT1JBVElPTjpOb25lfUE6YWN0aXZlIHsgICAgICBDT0xPUjojMDAwMDAwOyBURVhULURFQ09SQVRJT046Tm9uZX1BOmhvdmVyIHsgICAgQ09MT1I6IzAwOTlGRjsgVEVYVC1ERUNPUkFUSU9OOk5vbmV9PC9zdHlsZT48L3A+PHA+PGJyIC8+Jm5ic3A7PC9wPjx0YWJsZT48dGJvZHk+PHRyIGNsYXNzPSJmaXJzdFJvdyI+PHRkIHZhbGlnbj0idG9wIiB3aWR0aD0iMzcwIiBzdHlsZT0iYm9yZGVyLWJvdHRvbTogMHB4IHNvbGlkOyBib3JkZXItbGVmdDogMHB4IHNvbGlkOyBib3JkZXItdG9wOiAwcHggc29saWQ7IGJvcmRlci1yaWdodDogMHB4IHNvbGlkIj48cCBzdHlsZT0idGV4dC1hbGlnbjogY2VudGVyIj48YSB0YXJnZXQ9Il9zZWxmIiBocmVmPSJodHRwczovL3d3dy5sYW5kY2hpbmEuY29tLyI+PGltZyB0aXRsZT0idGRzY3dfbG9nZTEucG5nIiBhbHQ9InRkc2N3X2xvZ2UxLnBuZyIgc3JjPSJodHRwczovL3d3dy5sYW5kY2hpbmEuY29tL25ld21hbmFnZS91ZWRpdG9yL3V0ZjgtbmV0L25ldC91cGxvYWQvaW1hZ2UvMjAyMDA2MTAvNjM3Mjc0MDYzNDI4NzcxMTA4MTExMTMxMi5wbmciIC8+PC9hPjwvcD48L3RkPjx0ZCB2YWxpZ249InRvcCIgd2lkdGg9IjYyMCIgc3R5bGU9ImJvcmRlci1ib3R0b206IDBweCBzb2xpZDsgYm9yZGVyLWxlZnQ6IDBweCBzb2xpZDsgd29yZC1icmVhazogYnJlYWstYWxsOyBib3JkZXItdG9wOiAwcHggc29saWQ7IGJvcmRlci1yaWdodDogMHB4IHNvbGlkIj48c3BhbiBzdHlsZT0iZm9udC1mYW1pbHk6IOWui+S9kywgU2ltU3VuOyBjb2xvcjogcmdiKDI1NSwyNTUsMjU1KTsgZm9udC1zaXplOiAxMnB4Ij7kuLvlip7vvJroh6rnhLbotYTmupDpg6jkuI3liqjkuqfnmbvorrDkuK3lv4PvvIjoh6rnhLbotYTmupDpg6jms5XlvovkuovliqHkuK3lv4PvvIk8L3NwYW4+PHA+PHNwYW4gc3R5bGU9ImZvbnQtZmFtaWx5OiDlrovkvZMsIFNpbVN1bjsgY29sb3I6IHJnYigyNTUsMjU1LDI1NSk7IGZvbnQtc2l6ZTogMTJweCI+5oyH5a+85Y2V5L2N77ya6Ieq54S26LWE5rqQ6YOo6Ieq54S26LWE5rqQ5byA5Y+R5Yip55So5Y+4Jm5ic3A7ICZuYnNwO+aKgOacr+aUr+aMge+8mua1meaxn+iHu+WWhOenkeaKgOiCoeS7veaciemZkOWFrOWPuDwvc3Bhbj48L3A+PHA+PHNwYW4gc3R5bGU9ImNvbG9yOiAjZmZmZmZmIj48c3BhbiBzdHlsZT0iZm9udC1mYW1pbHk6IOWui+S9kywgU2ltU3VuOyBmb250LXNpemU6IDEycHgiPjxhIGhyZWY9Imh0dHBzOi8vYmVpYW4ubWlpdC5nb3YuY24vIj48c3BhbiBzdHlsZT0iY29sb3I6ICNmZmZmZmYiPuS6rElDUOWkhzEyMDM5NDE05Y+3LTQ8L3NwYW4+PC9hPjwvc3Bhbj48L3NwYW4+PHNwYW4gc3R5bGU9ImZvbnQtZmFtaWx5OiDlrovkvZMsIFNpbVN1bjsgY29sb3I6IHJnYigyNTUsMjU1LDI1NSk7IGZvbnQtc2l6ZTogMTJweCI+Jm5ic3A7Jm5ic3A7Jm5ic3A7PGEgaHJlZj0iaHR0cHM6Ly93d3cuYmVpYW4uZ292LmNuL3BvcnRhbC9yZWdpc3RlclN5c3RlbUluZm8/cmVjb3JkY29kZT0xMTAxMDIwMjAwODk5MCI+PHNwYW4gc3R5bGU9ImNvbG9yOiAjZmZmZmZmIj7kuqzlhaznvZHlronlpIcxMTAxMDIwMjAwODk5MDwvc3Bhbj48L2E+Jm5ic3A7Jm5ic3A7Jm5ic3A76YKu566x77yabGFuZGNoaW5hMjE4QDE2My5jb20mbmJzcDsmbmJzcDs8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCI+dmFyIF9iZGhtUHJvdG9jb2wgPSAoKCJodHRwczoiID09IGRvY3VtZW50LmxvY2F0aW9uLnByb3RvY29sKSA/ICIgaHR0cHM6Ly8iIDogIiBodHRwczovLyIpO2RvY3VtZW50LndyaXRlKHVuZXNjYXBlKCIlM0NzY3JpcHQgc3JjPSciICsgX2JkaG1Qcm90b2NvbCArICJobS5iYWlkdS5jb20vaC5qcyUzRjgzODUzODU5YzcyNDdjNWIwM2I1Mjc4OTQ2MjJkM2ZhJyB0eXBlPSd0ZXh0L2phdmFzY3JpcHQnJTNFJTNDL3NjcmlwdCUzRSIpKTs8L3NjcmlwdD48L3NwYW4+PC9wPjwvdGQ+PC90cj48L3Rib2R5PjwvdGFibGU+PHA+Jm5ic3A7PC9wPh8BBWRCQUNLR1JPVU5ELUlNQUdFOnVybChodHRwOi8vd3d3LmxhbmRjaGluYS5jb20vVXNlci9kZWZhdWx0L1VwbG9hZC9zeXNGcmFtZUltZy94X3Rkc2N3MjAxM195d18xLmpwZyk7ZGQ1z+V+RICZ0hssha+lKHWMz4GGht9DmlEQCTUCurTkBw==',
        '__VIEWSTATEGENERATOR': 'CA0B0334',
        '__EVENTVALIDATION': '/wEdAAL0+fvqyrVaZnjD+2HviN4aCeA4P5qp+tM6YGffBqgTjdd0BHni4HIQua7lA898YuFwdNE13bVW74kboq4JEJBg',
        'hidComName': 'default',
        'TAB_QuerySubmitConditionData': '',
        'TAB_QuerySubmitOrderData': '',
        'TAB_RowButtonActionControl': '',
        'TAB_QuerySubmitPagerData': i,
        'TAB_QuerySubmitSortData': ''

    }
    response = session.post(url="https://www.landchina.com/default.aspx?tabid=226", headers=headers,data=data,verify=False)
    html = etree.HTML(response.text)
    list = html.xpath(
        '//table[@id="TAB_contentTable"]/tbody//tr[@class="gridAlternatingItem"] |//table[@id="TAB_contentTable"]/tbody//tr[@class="gridItem"]')
    for item in list:
        try:
            number = item.xpath('./td[@class="gridTdNumber"]/text()')[0]
            SubList = item.xpath('./td[@class="queryCellBordy"]')
            location = SubList[0].xpath('text()')[0]
            href = "http://www.landchina.com/" + SubList[1].xpath('a/@href')[0]
            time = SubList[2].xpath('text()')[0]
            print(number, location, href, time)
        except:
            print("请求错误")
