# -*- encoding = utf-8 -*-
import time
from queue import Queue
from threading import Thread
import random
import requests
from lxml import etree
import os
import shutil
import re
import logging
import json
from ast import literal_eval
import pymongo

"""
@ mulitply threads spider 

@ author wxc
@  spider novels from the shuquge website 
"""

class novelSpider(object):
    def __init__(self,url,dir):
        self.ua_list = [
       "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36",
       "Mozilla/5.0 (Linux; Android 9; MI 9 SE Build/PKQ1.181121.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045111 Mobile Safari/537.36 MMWEBID/1500 MicroMessenger/7.0.11.1600(0x27000B33) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
       "Mozilla/5.0 (Linux; Android 9; V1838A Build/PKQ1.190302.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
       "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Plus Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.16 SP-engine/2.12.0 baiduboxapp/11.16.2.10 (Baidu; P1 7.1.1)",
       "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; OPPO R9tm Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36",
       "Mozilla/5.0 (Linux; Android 9; BND-AL00 Build/HONORBND-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.6 baiduboxapp/11.6.1.10 (Baidu; P1 9)",
       "Mozilla/5.0 (Linux; Android 9; MI 6X Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045111 Mobile Safari/537.36 MMWEBID/5003 MicroMessenger/7.0.11.1600(0x27000B33) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
       "Mozilla/5.0 (Linux; Android 9; CLT-TL00 Build/HUAWEICLT-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; MI 9 SE Build/PKQ1.181121.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045111 Mobile Safari/537.36 MMWEBID/1500 MicroMessenger/7.0.11.1600(0x27000B33) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 9; V1838A Build/PKQ1.190302.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Plus Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.16 SP-engine/2.12.0 baiduboxapp/11.16.2.10 (Baidu; P1 7.1.1)",
        "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; OPPO R9tm Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; BND-AL00 Build/HONORBND-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.6 baiduboxapp/11.6.1.10 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; MI 6X Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045111 Mobile Safari/537.36 MMWEBID/5003 MicroMessenger/7.0.11.1600(0x27000B33) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 9; CLT-TL00 Build/HUAWEICLT-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; FIG-TL10 Build/HUAWEIFIG-TL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.18 SP-engine/2.14.0 baiduboxapp/11.18.0.12 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; vivo X20 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/9.9 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 MicroMessenger/7.0.9(0x17000929) NetType/WIFI Language/zh_HK",
        "Mozilla/5.0 (Linux; Android 10; MI 9 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1169 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/4149 MicroMessenger/7.0.11.1600(0x27000B33) Process/tools NetType/4G Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 9; MI 8 Lite Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1169 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/673 MicroMessenger/7.0.11.1600(0x27000B33) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 9; PCAM00 Build/PKQ1.190519.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.11(0x17000b21) NetType/WIFI Language/zh_CN",
        "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-cn; ONEPLUS A5000 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.1.2; vivo X9i Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 7.1.2)",
        "Mozilla/5.0 (Linux; Android 9; SEA-AL10 Build/HUAWEISEA-AL1001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; MIX 2 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 10; V1914A Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 10)",
        "Mozilla/5.0 (Linux; U; Android 10; zh-cn; GM1910 Build/QKQ1.190716.003) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; GM1910 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045120 Mobile Safari/537.36 V1_AND_SQ_8.2.7_1334_YYB_D QQ/8.2.7.4410 NetType/WIFI WebP/0.3.0 Pixel/1440 StatusBarHeight/128 SimpleUISwitch/0",
        "Mozilla/5.0 (Linux; Android 9; V1838T Build/PKQ1.190302.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; PACT00 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; Android 10; LYA-TL00 Build/HUAWEILYA-TL00L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.2.2 (Baidu; P1 10)",
        "Mozilla/5.0 (Linux; Android 9; Mi9 Pro 5G Build/PKQ1.190714.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "(Linux; U; Android 8.0.0; zh-CN; VTR-AL00 Build/HUAWEIVTR-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.8.0.960 Mobile Safari/537.36",
        "Mozilla / 5.0(Linux; Android 5.1; PAR - AL00 Build / HUAWEIPAR - AL00; wv) AppleWebKit / 537.36(KHTML, like Gecko) Version / 4.0 Chrome / 62.0 .2627 .132 MQQBrowser / 6.2 TBS / 044304 Mobile Safari / 537.36 MicroMessenger / 6.7 .3 .1360(0x26070333) NetType / WIFI Language / zh_CN Process / tools",
        "Mozilla/5.0 (Linux; Android 5.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1550(0x26070333) NetType/WIFI Language/zh_CN Process/tools",
        "Mozilla/5.0 (Linux; Android 8.1; m2 note Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.0.0 Mobile MQQBrowser/6.2 TBS/036215 Safari/537.36 MicroMessenger/6.3.18.800 NetType/WIFI Language/zh_CN",
        "Mozilla/5.0 (Linux; Android 8.0; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2987.132 MQQBrowser/6.2 TBS/044353 Mobile Safari/537.36 MicroMessenger/6.7.3.1440(0x26070333) NetType/WIFI Language/zh_CN Process/tools",
        "Mozilla/5.0 (Linux; Android 9; PADM00 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.3359.126 MQQBrowser/6.2 TBS/045118 Mobile Safari/537.36 MMWEBID/4426 MicroMessenger/7.0.11.1600(0x27048B32) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; VTR-AL00 Build/HUAWEIVTR-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.8.0.960 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.0.0; VTR-AL00 Build/HUAWEIVTR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045120 Mobile Safari/537.36 V1_AND_SQ_8.2.0_1296_YYB_D QQ/8.2.0.4310 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/72 SimpleUISwitch/0",
        "Mozilla/5.0 (Linux; Android 9; ART-AL00x Build/HUAWEIART-AL00x; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; U; Android 9; zh-CN; MHA-TL00 Build/HUAWEIMHA-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.9.1069 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; HWI-AL00 Build/HUAWEIHWI-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1169 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/6714 MicroMessenger/7.0.11.1600(0x27000B35) Process/toolsmp NetType/WIFI Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 7.0; M654 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.12 baiduboxapp/11.12.0.10 (Baidu; P1 7.0)",
        "Mozilla/5.0 (Linux; Android 8.1.0; vivo Y83A Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; U; Android 9; zh-cn; Redmi Note 5 Build/PKQ1-wesley_iui-19.07.27) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.7.34",
        "Mozilla/5.0 (Linux; Android 10; VCE-AL00 Build/HUAWEIVCE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 10)",
        "Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57t Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.7 baiduboxapp/11.13.5.4 (Baidu; P1 6.0.1)",
        "Mozilla/5.0 (Linux; Android 9; JKM-TL00 Build/HUAWEIJKM-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 6.0.1; vivo Y66L Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 6.0.1)",
        "Mozilla/5.0 (Linux; Android 9; SEA-AL00 Build/HUAWEISEA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; U; Android 10; zh-CN; ONEPLUS A6000 Build/QKQ1.190716.003) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.9.1069 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; TAS-AN00 Build/HUAWEITAS-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045118 Mobile Safari/537.36 MMWEBID/4133 MicroMessenger/7.0.10.1580(0x27000AFE) Process/tools NetType/4G Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 8.1.0; JKM-AL00b Build/HUAWEIJKM-AL00b; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; Android 8.0.0; WAS-AL00 Build/HUAWEIWAS-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.0.0)",
        "Mozilla/5.0 (Linux; Android 7.1.1; vivo X20A Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.0.11 (Baidu; P1 7.1.1)",
        "Mozilla/5.0 (Linux; Android 9; MI 9 SE Build/PKQ1.181121.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1169 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/1500 MicroMessenger/7.0.11.1600(0x27000B33) Process/toolsmp NetType/WIFI Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 8.1.0; V1809A Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; Android 10; MI 8 UD Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 10)",
        "Mozilla/5.0 (Linux; U; Android 9; zh-cn; MI 9 SE Build/PKQ1.181121.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.8.12",
        "Mozilla/5.0 (Linux; U; Android 10; zh-CN; HMA-AL00 Build/HUAWEIHMA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.9.1069 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; CLT-AL01 Build/HUAWEICLT-AL01; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045118 Mobile Safari/537.36 MMWEBID/9071 MicroMessenger/7.0.10.1580(0x27000AFC) Process/tools NetType/4G Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 10; ELE-AL00 Build/HUAWEIELE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1168 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/742 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 10; ELE-AL00 Build/HUAWEIELE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1168 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/9724 MicroMessenger/7.0.10.1580(0x27000AFE) Process/tools NetType/4G Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/13.0 MQQBrowser/9.9.1 Mobile/15B87 Safari/604.1 QBWebViewUA/2 QBWebViewType/1 WKType/1",
        "Mozilla/5.0 (Linux; Android 10; YAL-AL00 Build/HUAWEIYAL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 10)",
        "Mozilla/5.0 (Linux; Android 10; YAL-AL10 Build/HUAWEIYAL-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/45016 Mobile Safari/537.36 MMWEBID/7181 MicroMessenger/7.0.10.1580(0x27000AFE) Process/tools NetType/4G Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 9; vivo NEX A Build/PKQ1.181030.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; JKM-AL00 Build/HUAWEIJKM-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; vivo Z1i Build/PKQ1.180819.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; U; Android 10; zh-CN; SEA-AL10 Build/HUAWEISEA-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.6.1036 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 10) NABar/1.0",
        "Mozilla/5.0 (Linux; Android 8.1.0; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; U; Android 10; zh-cn; Redmi K20 Pro Build/QKQ1.190825.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.8.12",
        "Mozilla/5.0 (Linux; Android 9; HRY-AL00Ta Build/HONORHRY-AL00Ta; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045118 Mobile Safari/537.36 MMWEBID/2904 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 9; PCHM10 Build/PKQ1.190714.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; U; Android 9; zh-cn; Redmi Note 7 Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.5.12",
        "Mozilla/5.0 (Linux; Android 9; meizu 16Xs Build/PKQ1.190302.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045118 Mobile Safari/537.36 MMWEBID/6051 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/4G Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 10; VCE-AL00 Build/HUAWEIVCE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045118 Mobile Safari/537.36 MMWEBID/4693 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/4G Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 6.0; OPPO A37t Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.10 baiduboxapp/11.10.0.12 (Baidu; P1 6.0)",
        "Mozilla/5.0 (Linux; U; Android 10; zh-cn; MI 8 Build/QKQ1.190828.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.8.14",
        "Mozilla/5.0 (Linux; Android 8.1.0; CMCC M761 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.10 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; Android 10; LYA-TL00 Build/HUAWEILYA-TL00L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1168 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/5060 MicroMessenger/7.0.11.1600(0x27000B32) Process/toolsmp NetType/WIFI Language/zh_CN ABI/arm64",
        "Mozilla/5.0 (Linux; Android 7.1.1; Mi Note 3 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 7.1.1)",
        "Mozilla/5.0 (Linux; U; Android 10; zh-cn; LYA-TL00 Build/HUAWEILYA-TL00L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 9; zh-CN; COR-AL10 Build/HUAWEICOR-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.9.1069 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/13.0 MQQBrowser/10.1.0 Mobile/15B87 Safari/604.1 QBWebViewUA/2 QBWebViewType/1 WKType/1",
        "Mozilla/5.0 (Linux; Android 9; ONEPLUS A6000 Build/PKQ1.180716.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; SKW-A0 Build/SKYW1905272CN00MP4; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; COR-AL10 Build/HUAWEICOR-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 9; Redmi 6 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/8967 MicroMessenger/7.0.11.1600(0x27000B32) Process/tools NetType/4G Language/zh_CN ABI/arm32",
        "Mozilla/5.0 (Linux; U; Android 9; zh-cn; COR-AL10 Build/HUAWEICOR-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/9.1 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; 1801-A01 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.0.1070 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 9; zh-cn; V1809A Build/PKQ1.181030.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; WLZ-AL10 Build/HUAWEIWLZ-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 10)",
        "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; Redmi 5A Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.8.14",
        "Mozilla/5.0 (Linux; Android 10; HRY-AL00Ta Build/HONORHRY-AL00Ta; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 10)",
        "Mozilla/5.0 (Linux; U; Android 1; zh-CN; MI 9S Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.6.1066 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.0.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.0.0)",
        "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; MI 5 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.3.0",
        "Mozilla/5.0 (Linux; Android 9; V1813BA Build/PKQ1.181030.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; U; Android 9; zh-CN; PAR-AL00 Build/HUAWEIPAR-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.9.1069 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; Redmi 8 Build/PKQ1.190319.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; U; Android 10; zh-cn; MI 9 Build/QKQ1.190825.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; LLD-AL20 Build/HONORLLD-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045111 Mobile Safari/537.36 MMWEBID/8227 MicroMessenger/7.0.10.1580(0x27000AFD) Process/tools NetType/WIFI Language/zh_CN ABI/arm64",
        ]
        self.url = url
        self.queue = Queue()
        self.proxy_list = literal_eval(requests.get("http://127.0.0.1:5010/get_all/").text)

        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db =  self.client.Spider
        self.collection = self.db.bZuserInfo

    def producer(self):
        total_num = 400000000
        for i in range(1, 3):
            self.queue.put("https://m.bilibili.com/space/" + str(i))
            
    def get_proxy(self):
        res = requests.get("http://127.0.0.1:5010/get_all/").text
        list = literal_eval(res)
        self.proxy_list =list

    def consumer(self):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                mid = url.replace('https://m.bilibili.com/space/', '')
                head = {'User-Agent': random.choice(self.ua_list),
                        'X-Requested-With': 'XMLHttpRequest',
                        'Origin': 'http://space.bilibili.com',
                        'Host': 'm.bilibili.com',
                        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Referer': "https://space.bilibili.com/",
                        }

                if(int(mid)%100==0):
                    self.get_proxy()
                proxy = random.choice(self.proxy_list)
                proxies = {"http": "http://{}".format(proxy)}
                time.sleep(random.randrange(1,5))
                try:
                    html = requests.get(url, headers=head, timeout=10,proxies=proxies).text
                    if html.find("window.__INITIAL_STATE__=") == -1:
                        return
                    formats = re.findall(r"window.__INITIAL_STATE__=(.*?);\(function\(\)", html)
                    try:
                        data = json.loads(formats[0])["space"]
                        name = data["info"]['name']
                        sex = data["info"]['sex']
                        face = data["info"]['face']
                        level = data['info']['level']
                    except:
                        pass
                    head = {'User-Agent': random.choice(self.ua_list),
                            'X-Requested-With': 'XMLHttpRequest',
                            'Origin': 'http://space.bilibili.com',
                            'Host': 'api.bilibili.com',
                            'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
                            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
                            'Accept': 'application/json, text/javascript, */*; q=0.01',
                            'Referer': url}
                    res = requests.get('https://api.bilibili.com/x/relation/stat?jsonp=jsonp&vmid=' + str(mid),
                                       headers=head, timeout=10,proxies=proxies).text
                    res_js = json.loads(res)
                    following = res_js['data']['following']
                    follower = res_js['data']['follower']
                    print ( mid, name, sex, following, follower, level,face)
                    userInfo ={}
                    userInfo["mid"] =mid
                    userInfo["name"] =name
                    userInfo["sex"] =sex
                    userInfo["url"] =url
                    userInfo["level"] =level
                    userInfo["face"] =face
                    userInfo["following"] =following
                    userInfo["follower"] =follower
                    self.collection.insert_one(userInfo)
                except Exception as e:
                    logging.error('error in run function: ' + str(e))
                    return
            except:
                print(url +"has some wrong!")
    def main(self):
        t1 = Thread(target=self.producer)
        t1.start()
        time.sleep(5)
        for index in range(5):
            t2 = Thread(target=self.consumer)
            t2.start()
        t1.join()

if __name__ == '__main__':
    # please attentiom to the url form of novel form shuquge website
    Siper=novelSpider("http://www.shuquge.com/txt/8659/","novels")
    Siper.main()

