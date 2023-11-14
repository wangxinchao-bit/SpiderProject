import pickle
import requests
from requests import Session

# 创建一个新的 Session 对象
session = Session()
# 从文件中加载 cookie
with open('login/zhcookies.cookie', 'rb') as f:
    loaded_cookies = pickle.load(f)

# 将加载的 cookie 设置到 Session 对象中
session.cookies.update(loaded_cookies)
cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
