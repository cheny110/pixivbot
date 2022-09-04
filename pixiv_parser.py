
from threading import Thread
from requests import Session
from headers import header
import json
import os
from lxml import etree

image_base_url="https://i.pximg.net/img-master"
profile_base_url='https://www.pixiv.net/ajax/user/{}/profile/all?lang=en'


pixivSession=Session()
pixivSession.headers=header
    


class ImageItem():
    def __init__(self,name,sourceUrl,imgtype,savePath) -> None:
        self.name=name
        self.url=sourceUrl
        self.type=imgtype
        self.savePath=savePath
        self.coroutine=Thread(target=self.download)
    

    def download(self):
        response=pixivSession.get(self.url)
        #print(response.headers)
        with open(os.path.join(self.savePath,self.name.replace('/','')+'.'+self.type),'wb')as f:
            f.write(response.content)
            f.close



def parseRankImg(rankMode="daily",base_save_path=None):
    '''
    support rankMode : daily, weekly,monthly
    '''

    from datetime import datetime
    date=datetime.now().strftime("%Y_%m_%d")
    if rankMode=="daily":
        base_save_path=os.path.join("./",date+'_daily')
    elif rankMode=="weekly":
        base_save_path=os.path.join('./',date+'_weekly')
    else:
        base_save_path=os.path.join('./',date+'_monthly')
    resp=pixivSession.get("https://www.pixiv.net/ranking.php?mode={}&content=illust&ref=rn-h-image-3".format(rankMode))
    html=etree.HTML(resp.text)
    elements=html.xpath("// div[@class='_layout-thumbnail']/img/@data-src")
    names=html.xpath("// h2/a[@href]/text()")
    images=[element.split('img-master')[-1]for element in elements]
    image_urls=[image_base_url+image for image in images]
    types=[i.split('.')[-1]for i in image_urls]
    if not os.path.exists(base_save_path):
        os.makedirs(base_save_path)
    for i in range(len(image_urls)):
        ImageItem(names[i],image_urls[i],types[i],base_save_path).coroutine.run()


def parseImageByUserId(userId:str="2568265",base_save_path=None):
    resp=pixivSession.get("https://www.pixiv.net/ajax/user/{}/profile/top?lang=en".format(userId))  
    contents=json.loads(resp.text)
    illustsIds=list(contents["body"]["illusts"].keys())
    urls=[contents["body"]["illusts"][i]['url']for i in illustsIds]
    processedUrls=[i.replace("c/250x250_80_a2/","").replace("square","master")for i in urls]
    types=[i.split('.')[-1]for i in processedUrls]
    names=urls=[contents["body"]["illusts"][i]['title']for i in illustsIds]
    if not os.path.exists(base_save_path):
        os.makedirs(base_save_path)
    for i in range(len(names)):
        ImageItem(names[i],processedUrls[i],types[i]).coroutine.run()



def parseImageByUserName(name:str='ajimita',base_save_path=None):
    base_save_path=os.path.join("./",name)
    pixivSession.headers["referer"]="https://www.pixiv.net/en/tags/ajimita/artworks?s_mode=s_tag"
    pixivSession.headers["path"]="/search_user.php?nick=ajimita&s_mode=s_usr"
    pixivSession.headers["sec-fetch-mode"]="navigate"
    pixivSession.headers["sec-fetch-user"]="?1"
    pixivSession.headers["accept"]="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    pixivSession.headers["sec-fetch-dest"]="document"
    pixivSession.headers["cookie"]="_fbp=fb.1.1659602993795.311214565; _gcl_au=1.1.546577043.1661329323; a_type=0; b_type=1; c_type=23; device_token=1a6b19db6d3776adf867f8b44b94f6d8; p_ab_d_id=1764685532; p_ab_id=6; p_ab_id_2=7; PHPSESSID=55920084_KJyQmcUsdQH7EuK7rVriISmF2oNPRKMJ; privacy_policy_agreement=5; privacy_policy_notification=0; _im_vid=01G9M0WKPPEGHXA62TCA39JP25; first_visit_datetime_pc=2022-08-04+17:49:14; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; yuid_b=NllSZIQ; login_ever=yes; __utmv=235335808.|2=login ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=55920084=1^9=p_ab_id=6=1^10=p_ab_id_2=7=1^11=lang=en=1; tag_view_ranking=Lt-oEicbBr~RTJMXD26Ak~PTyxATIsK0~65aiw_5Y72~LtW-gO6CmS~XDEWeW9f9i~EUwzYuPRbU~pzzjRSV6ZO~FDjoZw3kaU~Xg4Yju42cN~ay54Q_G6oX~0aWE2bl15g~C9_ZtBtMWU~LJo91uBPz4~Ie2c51_4Sp~pnCQRVigpy~N0yI5Cxu-1~HY55MqmzzQ~nQRrj5c6w_~5AKOA9olwV~YRDwjaiLZn~qtVr8SCFs5~kP7msdIeEU~OT4SuGenFI~kMjNs0GHNN~ZXFMxANDG_~I5npEODuUW~K8esoIs2eW~jPsOGzt9Dh~_NKuYeNwHY~vKaV_Lyk9X~teRKye7Qbz~RybylJRnhJ; _gid=GA1.2.1416601000.1661605838; __utma=235335808.1906988987.1659602961.1661605822.1661679470.7; __utmc=235335808; __utmz=235335808.1661679470.7.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided); __utmt=1; __cf_bm=Em5UKQqfplonn.zO11NgqYJ2TY3srr.G6LIYvUAGA_Y-1661679520-0-AS1fxTW0NyY3FD7yVu0ep+KYSNrmLmv97JEMiH3wH2wmjaRFeLcgK9Uvv/QkpQ6qmLM/gjAjw4fp5atv6jkoSbDNfyLzzT6s+qIFDIe382G6qROjpO1F5pKfFaJ/n7gFsyJGmCayG4WJ6alBkU0nDbU=; cto_bundle=g3tpHF9tV2xRWHhUbm1HU3VWRnM1WmZ6bVlRV3o1c2l3VDQzbjBRNVVuWmREcURGNWdqWDRpdXJFQ25rRHAyaWFNd1NPQ29sTDdtMnUwWDdSYURUVEdoc3JwNW14blMyS00xMGVnWDhVTThQVGFoeXFRVFJzZWFsbHp3VzQlMkZOejhpdCUyQmVEVmxrd0l0UTgwN0wxOUlDN1lOYmJRJTNEJTNE; _ga=GA1.1.687805461.1659602961; __utmb=235335808.9.10.1661679470; _ga_75BBYNYN9J=GS1.1.1661679473.7.1.1661679802.0.0.0"
    resp=pixivSession.get("https://www.pixiv.net/search_user.php?nick={}&s_mode=s_usr".format(name))
    html=etree.HTML(resp.text)
    userId=html.xpath("//a[@href][@class='title']/@href")[-1].split('/')[-1]
    parseImageByUserId(userId,base_save_path)



if __name__=="__main__":
   parseRankImg("weekly")


