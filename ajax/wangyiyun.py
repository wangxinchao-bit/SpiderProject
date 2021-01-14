
import requests
import json

class wyxmusicSpider(object):
    def __init__(self):
        self.url ="https://interface.music.163.com/weapi/v6/playlist/detail"

        self.headers ={
            'origin': 'https://y.music.163.com',
            "referer": "https://y.music.163.com/",
            "cookie":"_ntes_nnid=c62f6033d7f797c4ada53e8a1aac7cd0,1610524589782; _ntes_nuid=c62f6033d7f797c4ada53e8a1aac7cd0; unisdk_udid=fb296286e56bc8350d877e783456d943; UM_distinctid=176ffa0939544c-039a3829c6c218-c791039-144000-176ffa09396bdb; NMTID=00OqObhWiZW6ekZE0_Cm2D7fh4XciIAAAF3AVPppQ; WEVNSM=1.0.0; WNMCID=pchouy.1610635012208.01.0; JSESSIONID-WYYY=vNpO0GytSeMft2NqAmy1FiYV2BcTudi9sRiI5%2Fv6b3c9S7Ansk48%5C2N1TflN4ZHx%2FVM%2BPe6t52c2XosEVDZEOI%2F7iYUhHiS36P%2BbYyxKYlp8ZIg0KF0VwOfHCUJFa2%5CNbB0iTgOGQ1N%5CF6VMh5wrt8RRKM5knhD%2F171NWvQ8g%5CxPoVRI%3A1610636854231; _iuqxldmzr_=33"
            }
        self.data = {
            "params": "EgkSpClwlpRp0kscmtmtlvwieQSlwn4TG7FNj/El+s14pWudL36jbZVSxPs2pVyQcg6Zji0p6JXXuIkY7ricPhF4oNSqQhk5fTFnkdgSByg=",
            "encSecKey": "2b7a1cf182c190c74ad38e28a4b07dea2f146a9d22150521f823108a04b265aa32f80eeb9578d0050965b09ddeeb1c69b7041ab77b2047246077202a8b5fe3349d6a61037a1073935abb80e88734e6186681ffd99b16e407591cabd7c3f50ea8d4a94b8dad5c41892f14297413d2496db4132fac3c4c4a34b689d69f9dcb7e14"
        }

    def get_page(self):
        i = 1
        res = requests.post(url =self.url,headers= self.headers,data= self.data)
        list = json.loads(res.text)["playlist"]['tracks']
        for item in list:
            try:
                name = item['name']
                id = item["id"]
                picUrl = item["al"]['picUrl']
                print(i,name,id,picUrl)
            except:
                pass
            i+=1
    def main(self):
        self.get_page()

if __name__ == '__main__':
    wyxmusic =wyxmusicSpider()
    wyxmusic.main()