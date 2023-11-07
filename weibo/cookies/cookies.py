import requests
import pickle

# 创建一个Session对象
session = requests.Session()

# 发送GET请求，获取Cookies
response = session.get('https://example.com')

# 保存Cookies到.cookie文件
with open('cookies.cookie', 'wb') as cookie_file:
    pickle.dump(session.cookies, cookie_file)

print(session.cookies)