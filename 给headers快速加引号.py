import re
headers ="""
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: max-age=0
content-length: 4740
content-type: application/x-www-form-urlencoded
cookie: Hm_lvt_83853859c7247c5b03b527894622d3fa=1611367869; ASP.NET_SessionId=iagfv5nrwwjpc1g35bo2cdul; Hm_lpvt_83853859c7247c5b03b527894622d3fa=1611368195
origin: https://www.landchina.com
referer: https://www.landchina.com/default.aspx?tabid=263&ComName=default
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36
"""
header =""
for i in headers:
    if i=='\n':
        i = "',\n'"

    header +=i
header=re.sub(': ',"': '",header)
ret = header[2:].replace(' ','')+'\''
print(ret[:-4])