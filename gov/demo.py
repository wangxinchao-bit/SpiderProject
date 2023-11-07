
import time
import execjs
import requests
import base64
from Crypto.Cipher import AES
import json
 
 
json_data = {
    'pageNo': 1,
    'pageSize': 20,
 
    'AREACODE': '',
    'M_PROJECT_TYPE': '',
    'KIND': 'GCJS',
    'GGTYPE': '1',
    'PROTYPE': '',
    'timeType': '6',
    'BeginTime': '2022-10-10 00:00:00',
    'EndTime': '2023-04-10 23:59:59',
    'createTime': [],
    'ts': int(round(time.time() * 1000)),
 
}

json_data = {
    "ts": round(time.time()*1000), "type":"fwsysdic20211012"
}
JsFile = open('fujian1.js', encoding='utf-8')
JsCode = JsFile.read()
compile_JsCode = execjs.compile(JsCode)
ParameterData = compile_JsCode.call('d', json_data)
 
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
response = requests.post('https://ggzyfw.fujian.gov.cn/FwPortalApi/Common/SysDic', headers=headers, json=json_data)

print(response.text)

def pkcs7unpadding(text):
    try:
        length = len(text)
        unpadding = ord(text[length-1])
        return text[0:length-unpadding]
    except Exception as e:
        pass

def aes_decode( content):
    key = 'BE45D593014E4A4EB4449737660876CE'
    key_bytes = bytes(key, encoding='utf-8')
    iv = b'A8909931867B0425'
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    aes_encode_bytes = base64.b64decode(content)
    aes_decode_bytes = cipher.decrypt(aes_encode_bytes)
    result = str(aes_decode_bytes, encoding='utf-8')
    result = pkcs7unpadding(result)
    return result
res  = aes_decode(response.json()["Data"])