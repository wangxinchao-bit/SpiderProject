
import time
import execjs
import requests
import base64
from Crypto.Cipher import AES
 

JsFile = open('fujian1.js', encoding='utf-8')
JsCode = JsFile.read()
compile_JsCode = execjs.compile(JsCode)

test = {
    "ts": round(time.time()*1000), "type":"fwsysdic20211012"
}
ParameterData = compile_JsCode.call('d', test)
 
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6,ru;q=0.5,fr;q=0.4,de;q=0.3',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://ggzyfw.fujian.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://ggzyfw.fujian.gov.cn/business/list/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'portal-sign': ParameterData,
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
response = requests.post('https://ggzyfw.fujian.gov.cn/FwPortalApi/Common/SysDic', headers=headers, json=test)

print(response.text)

