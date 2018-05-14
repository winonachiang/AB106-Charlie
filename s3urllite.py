import glob
import urllib.parse
import tldextract
from newspaper import Article
import time
t = time.time()
from datetime import datetime
import re
import hashlib
from pymongo import MongoClient
import pymongo
try:
    client = MongoClient('10.140.0.7', 27017) #10.140.0.7
    db = client['dsp_url'] #連結到mongoDB裡的database
    # to_redis = db['test_urls_o'] #這是DSP曝光url待爬中的
    collection = db['newcrawler01'] #這是DSP曝光url待爬中的
    # collection2 = db['newcrawler02']
    # collection3 = db['newcrawler03']
    # collection4 = db['newcrawler04']
    # collection5 = db['newcrawler05']
    # collection6 = db['newcrawler06']
    # collection7 = db['newcrawler07']
    # collection8 = db['newcrawler08']
    # collection9 = db['newcrawler09']
    # collection10 = db['newcrawler10']
    # collection11 = db['newcrawler11']
    # collection12 = db['newcrawler12']
    # collection13 = db['newcrawler13']
    # collection14 = db['newcrawler14']
    # collection15 = db['newcrawler15']
    # collection16 = db['newcrawler16']
    # collection17 = db['newcrawler17']
    # collection18 = db['newcrawler18']
    # collection19 = db['newcrawler19']
    # collection20 = db['newcrawler20']
except:
    print('Cannot connect to MongoDB server!')

unwanted = ['ibowbow.com','eyeprophet.com','styletc.com','blogspot.my','gamebase.com.tw','519640.com','atoomu.com',
'comicbus.com','popo.tw','mark6.online','millionbook.net','twjoin.com','mowd.tw','myself-bbs.com',
'rti.org.tw','168abc.net','4freeapp.com','ecnow.tw','googleadservices.com','penpal.tw','picsee.pro',
'pics.ee','doubleclick.net','fharr.com','blogspot.hk','systranlinks.net','soft8ware.com','softblog.tw',
'tnews.cc','googleusercontent.com','itver.cc','8shuw.net','bring-you.info','appspot.com','vtwtv.net',
'kanfb.com','enjoy101.org','vigortv.net','abacus.org.tw','fengbau.com','ibody.com.tw','isay.cc','lifeplus.com.tw',
'noblemusic.com.tw','blogspot.jp','localhost.','tvbstv.com','i-furkid.com','dolifeup.com','milkxtw.com',
'news98.com.tw','blogspot.sg','sitemaji.com','dfunmag.com.tw','swiftcode.info','msn.com','bingj.com',
'yidas.com','loltube.cc','hhh188.cn','dichtienghoa.com','simontamhk.com','qll.co','blogspot.ca','eazon.com',
'myyoudao.com','168abc.com.tw','oboo.info','cht.com.tw','E.','889house.info','192.168.0.144.','blogspot.cl',
'192.168.1.16.','blogspot.in','tarotbp.com','playlotto.cc','local.','xinguge.com','animalcloud.com.tw',
'c9users.io','nova.tw','docker8.','critical.tw','chinaproxy.club','ttnmedia.com.tw','docker9.','toolur.com',
'gotojojo.com','rate.cx','192.168.1.63.','crushus.com','gamedb.com.tw','blogspot.ae','wooquiz.com','uoo.',
'blogspot.qa','blogspot.mx','null.','203.66.83.93.','blogspot.ie','bridgewell.com','pocketimes.my',
'36.7.150.150.','sexav-123.com','lazyweb.net.tw','houseinfo.tw','world-check.com','itbase.com.tw',
'youfind.hk','evernote.com','210.61.2.86.','open.tips','dice01.com','vimeo.com','vietphrase.info','http://blogspot.gr',
'adsame.com','juding1.com','192.168.1.25.','blogspot.nl','104.199.139.109.','aqiusha.xyz','piee.pw',
'brianview.com','103.61.138.108.','sanlih.com.tw','wp.me','192.168.1.30.','eacloud.ml','anyproxy.top',
'blogspot.se','cpcg.ga','dongtaiwang.com','H.','blogspot.ro','aity.org','nova.net.tw','blogspot.com.eg',
'muza-art.com','informationvine.com','60.251.178.185.','pis.li','yangfengwuzhi.com','G.','lnk.pics',
'toolskk.com','mixrent.com','v.gd','192.168.1.73.','keeplay.net','pixanalytics.com','99770.cc','car2taiwan.com',
'jimeru.com','twtimes.com.tw','C.','blank.','122.146.248.162.','darkwing.co','blogspot.pe','tvshowbox.tw',
'google.com','isinchu.com','papbear.com','peggyli.tw','ukpa99.com','atoomu.xyz','enrich168.com','divers123.com',
'ehoho.com','mydowndown.com','paochen.com.tw','ckpa99.com','googlesyndication.com','ccii.com.tw','dribs-drabs.com',
'hiweb.tw','goodface.tw','onmypc.us','codepen.io','fimmediaasia.com','s6law.net','nantou.com.tw',
'loveplay123.com','wheresupermarket.com','.','67.215.246.150.','baidu.com','mrq.tw','nett.com.tw','contents.',
'blogspot.com.au','fengyuncai.com','tai-chung.com.tw','estock.com.tw','com.fi','D.','hoho.tw','menubar.tw',
'herokuapp.com','aimying.com','flash4u.com.tw','amazonaws.com','bluezz.com.tw','blogspot.cz','skyeyes.tw',
'5299.com.tw','6law.idv.tw','85novel.com','aka99.com','arms-cool.net','arthurtoday.com','baibai.com.tw',
'bcc.com.tw','biza.com.tw','centerbbs.com','www.com.tw','crazy-tutorial.com','daybuy.tw','dk101.com',
'doujin.com.tw','eee-learning.com','enjoyfood.com.tw','find3cshop.com','game735.com','ichacha.net','icourse.com.tw',
'lbj.tw','lotto-8.com','lottonavi.com','makezine.com.tw','manga.hk','money511.com','mp3.net.tw','mxp.tw',
'mygopen.com','ncc.com.tw','penghutimes.com','pilio.idv.tw','playsport.cc','flip.it','test.','192.168.53.92.',
'amazon.de','6039','113.196.127.201.','maxfoodfun.com','prettyma3c.com.tw','tubeoffline.com','tellustek.com.tw',
'192.96.205.5.','unmht.','jshell.net','192.168.70.84.','106.14.168.11.','public.tw','net%2Farticles%2F51195.',
'192.168.1.60.','192.168.10.92.','macworld.co.uk','baiducontent.com','freejobalert.com','blogspot.co.nz',
'bild.de','60.251.117.74.','pcworld.com','54.92.61.95.','6424','soft4fun.net','aaa.com','opoint.com',
'wnd.com','topmedia.com.tw','4000015888.com','house-info.com.tw','9900.com.tw','210.61.47.163.',
'legacy.com','oysjewelry.com','rungobm.com','doublemax.net','127.0.0.1.','blogspot.tw','202.39.224.10.',
'4fun.tw','pts.org.tw','roodo.com','doublemax.net','aralego.com','animalcollege.org','anixwallpaper.com',
'appier.net','appinc.org','b111.net','bassavg.com','bbs-mychat.com','flash2u.com.tw','kimy.com.tw','mlwd.com.tw',
'mychat.to','tw789.net','ctitv.com.tw','8shuw.com','biga.com.tw','bingfeng.tw','hellosanta.com.tw',
'mixflavor.com','freebbs.tw','bookmarks.tw','cccsub.com','cdnews.biz','cherry123.com','chinaqna.com',
'kpopstarz.cn','ck101.com','acgn.cc','pros.ee','adnw.xyz','appinn.com','digitalwall.com','disp.cc',
'qooah.com','pili.com.tw','ebptt.com','marbo.com.tw','eznewlife.com','ezwebin.com','flog.tw','flycall.com',
'svu.com.tw','skm.com.tw','findx2.net','fws.tw','mewmew.xyz','goo.gl','bit.ly','hotelnews.tw','file.',
'libertyocean.com','comicvip.com','unblocksites.co','pwserv.com','cartoonmad.com','blogspot.de',
'66ghz.com','syncupwithuniverse.com','ilovedrum.com','tw116.com','vtwtv.com','211.20.236.22.','hhxxee.com',
'dler.org','renwun-digital.com','adnxs.com','cloudapp.net','172.16.1.98.','61.219.29.200.','blogspot.be',
'ek21.com','kpopstarz.com.cn','xn--2qq421aovbc9ak04b.com','google.co.jp','google.com.tw','10.227.170.99.',
'120.104.18.185.','smartnet.tw','zgtlgg.net','211.20.120.100.','arlentung.idv.tw','flbk.com.tw',
'sex-dr.com','blogspot.fr','facebook.com','e-stock.com.tw','emp834.idv.tw','hobbycouple.com','blogspot.it',
'komica.org','naver.net','life101.com.tw','loaner.taipei','more.game.tw','blogspot.com.es','hhmmoo.com',
'61.221.141.45.','pise.pw','videobowbow.com','loltube.tw','192.168.1.17.','10001mb.com','99manga.com',
'filesusr.com','mychat.tw','ziqiang.tw','my-style.in','coffeehighfive.com','blogspot.kr','inskinmedia.com',
'archive.org','allsharer.com','dmeden.net','tellustek.com','888stock.idv.tw','F.','68xi.cn','editmysite.com',
'advenueplatform.com','google.com.hk','cai1991.tw','thebeerissue.com.tw','blogspot.ru','kokoha.tw',
'jjdtbb.com','funuv.com','blogspot.com.br','hioselect.com','lifer.tw','pice.pw','updog.co','blogspot.ch',
'blogspot.co.id','lifefree.com.tw','puunitedstates.cn','html.','nosejobtaiwan.com','cgbap.com','golinksafe.com',
'txmblr.com','i-gamer.net','illu.es','jiaafrica.cn','wornhole1.cn','psee.io','statictab.com','hifulift.com',
'goog_content.','pchome.com.tw','hinet.net','weibo.com','blueshop.com.tw','chtoen.com','wewanted.com.tw',
'twocomic.com','sixcomic.com','qidian.com.tw','plurk.com','zipko.info','www.vtwtv.net','http://quiz321.com',
'http://sixcomic.com','taiwantimes.com.tw','truthmall.com','ttv.com.tw','uho.com.tw','wherebank.com',
'wownews.tw','informagnet.com','172.17.0.2.','funnyp.online','kukuru.tw','caca01.com','smady.com',
'mmweb.tw','youbike.com.tw','1989wolfe.com','olgclub.com','translatoruser.net','xxlbasketball.com.tw',
'210.243.166.51.','urmay.com','chihchih.net','bzhotel.com.tw','crazyall.net','googleapis.com','jollygoodkangaroo.com',
'weebly.com','watchinese.com','niotv.com','mydesy.com','hhh.com.tw','ustv.com.tw','truemovie.com']

print('start sending url to mongoDB')
start = time.time()
def tomd5(url):
    hash_object = hashlib.md5(url.encode())
    MD5code = hash_object.hexdigest()#將url轉成MD5並且存取下來
    return MD5code

list_of_files = glob.glob("/home/c29559810/s3/impression_urls/*_0") #D:\\s3\\0506\\*_0
print("start sending to our database") #
i = 1
for file_name in list_of_files:
    fi = open(file_name,"r")
    urls = {}
    for line in fi:
        singleurl = "http://"+ line.rstrip().replace('|','')
        urls['url'] = singleurl
        urls['_id'] = tomd5(singleurl)
        decodedurl = urllib.parse.unquote(singleurl) #把encode的url先decode
        list = tldextract.extract(decodedurl)
        domain_name = list.domain + '.' + list.suffix
        urls['from'] = domain_name
        if urls['from'] in unwanted:
            pass
        else:
            urls['for'] = 'crawler' + str(i)
            if i < 54:
                i += 1
            else:
                i = 1
            try:
                collection.insert_one(urls)
            except:
                pass
end = time.time()
elapsed = end - start
print('all sent')
print ("Time taken: ", elapsed, "seconds.")
# for file_name2 in list_of_files[5:8]:
#     fi2 = open(file_name2,"r")
#     urls2 = {}
#     for line2 in fi2:
#         singleurl2 = "http://" + line2.rstrip().replace('|','')
#         urls2['url'] = singleurl2
#         urls2['_id'] = tomd5(singleurl2)
#         decodedurl2 = urllib.parse.unquote(singleurl2) #把encode的url先decode
#         list2 = tldextract.extract(decodedurl2)
#         domain_name2 = list2.domain + '.' + list2.suffix
#         urls2['from'] = domain_name2
#         urls2['for'] = 'crawler02'
#         if urls2['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls2)
#             except:
#                 pass

# for file_name3 in list_of_files[9:12]:
#     fi3 = open(file_name3,"r")
#     urls3 = {}
#     for line3 in fi3:
#         singleurl3 = "http://" + line3.rstrip().replace('|','')
#         urls3['url'] = singleurl3
#         urls3['_id'] = tomd5(singleurl3)
#         decodedurl3 = urllib.parse.unquote(singleurl3) #把encode的url先decode
#         list3 = tldextract.extract(decodedurl3)
#         domain_name3 = list3.domain + '.' + list3.suffix
#         urls3['from'] = domain_name3
#         urls3['for'] = 'crawler03'
#         if urls3['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls3)
#             except:
#                 pass

# for file_name4 in list_of_files[13:16]:
#     fi4 = open(file_name4,"r")
#     urls4 = {}
#     for line4 in fi4:
#         singleurl4 = "http://" + line4.rstrip().replace('|','')
#         urls4['url'] = singleurl4
#         urls4['_id'] = tomd5(singleurl4)
#         decodedurl4 = urllib.parse.unquote(singleurl4) #把encode的url先decode
#         list4 = tldextract.extract(decodedurl4)
#         domain_name4 = list4.domain + '.' + list4.suffix
#         urls4['from'] = domain_name4
#         urls4['for'] = 'crawler04'
#         if urls4['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls4)
#             except:
#                 pass

# for file_name5 in list_of_files[17:20]:
#     fi5 = open(file_name5,"r")
#     urls5 = {}
#     for line5 in fi5:
#         singleurl5 = "http://" + line5.rstrip().replace('|','')
#         urls5['url'] = singleurl5
#         urls5['_id'] = tomd5(singleurl5)
#         decodedurl5 = urllib.parse.unquote(singleurl5) #把encode的url先decode
#         list5 = tldextract.extract(decodedurl5)
#         domain_name5 = list5.domain + '.' + list5.suffix
#         urls5['from'] = domain_name5
#         urls5['for'] = 'crawler05'
#         if urls5['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls5)
#             except:
#                 pass

# for file_name6 in list_of_files[21:24]:
#     fi6 = open(file_name6,"r")
#     urls6 = {}
#     for line6 in fi6:
#         singleurl6 = "http://" + line6.rstrip().replace('|','')
#         urls6['url'] = singleurl6
#         urls6['_id'] = tomd5(singleurl6)
#         decodedurl6 = urllib.parse.unquote(singleurl6) #把encode的url先decode
#         list6 = tldextract.extract(decodedurl6)
#         domain_name6 = list6.domain + '.' + list6.suffix
#         urls6['from'] = domain_name6
#         urls6['for'] = 'crawler06'
#         if urls6['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls6)
#             except:
#                 pass

# for file_name7 in list_of_files[25:28]:
#     fi7 = open(file_name7,"r")
#     urls7 = {}
#     for line7 in fi7:
#         singleurl7 = "http://" + line7.rstrip().replace('|','')
#         urls7['url'] = singleurl7
#         urls7['_id'] = tomd5(singleurl7)
#         decodedurl7 = urllib.parse.unquote(singleurl7) #把encode的url先decode
#         list7 = tldextract.extract(decodedurl7)
#         domain_name7 = list7.domain + '.' + list7.suffix
#         urls7['from'] = domain_name7
#         urls7['for'] = 'crawler07'
#         if urls7['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls7)
#             except:
#                 pass

# for file_name8 in list_of_files[29:32]:
#     fi8 = open(file_name8,"r")
#     urls8 = {}
#     for line8 in fi8:
#         singleurl8 = "http://" + line8.rstrip().replace('|','')
#         urls8['url'] = singleurl8
#         urls8['_id'] = tomd5(singleurl8)
#         decodedurl8 = urllib.parse.unquote(singleurl8) #把encode的url先decode
#         list8 = tldextract.extract(decodedurl8)
#         domain_name8 = list8.domain + '.' + list8.suffix
#         urls8['from'] = domain_name8
#         urls8['for'] = 'crawler08'
#         if urls8['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls8)
#             except:
#                 pass

# for file_name9 in list_of_files[33:36]:
#     fi9 = open(file_name9,"r")
#     urls9 = {}
#     for line9 in fi9:
#         singleurl9 = "http://" + line9.rstrip().replace('|','')
#         urls9['url'] = singleurl9
#         urls9['_id'] = tomd5(singleurl9)
#         decodedurl9 = urllib.parse.unquote(singleurl9) #把encode的url先decode
#         list9 = tldextract.extract(decodedurl9)
#         domain_name9 = list9.domain + '.' + list9.suffix
#         urls9['from'] = domain_name9
#         urls9['for'] = 'crawler09'
#         if urls9['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls9)
#             except:
#                 pass

# for file_name10 in list_of_files[37:40]:
#     fi10 = open(file_name10,"r")
#     urls10 = {}
#     for line10 in fi10:
#         singleurl10 = "http://" + line10.rstrip().replace('|','')
#         urls10['url'] = singleurl10
#         urls10['_id'] = tomd5(singleurl10)
#         decodedurl10 = urllib.parse.unquote(singleurl10) #把encode的url先decode
#         list10 = tldextract.extract(decodedurl10)
#         domain_name10 = list10.domain + '.' + list10.suffix
#         urls10['from'] = domain_name10
#         urls10['for'] = 'crawler10'
#         if urls10['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls10)
#             except:
#                 pass

# for file_name11 in list_of_files[41:44]:
#     fi11 = open(file_name11,"r")
#     urls11 = {}
#     for line11 in fi11:
#         singleurl11 = "http://" + line11.rstrip().replace('|','')
#         urls11['url'] = singleurl11
#         urls11['_id'] = tomd5(singleurl11)
#         decodedurl11 = urllib.parse.unquote(singleurl11) #把encode的url先decode
#         list11 = tldextract.extract(decodedurl11)
#         domain_name11 = list11.domain + '.' + list11.suffix
#         urls11['from'] = domain_name11
#         urls11['for'] = 'crawler11'
#         if urls11['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls11)
#             except:
#                 pass

# for file_name12 in list_of_files[45:48]:
#     fi12 = open(file_name12,"r")
#     urls12 = {}
#     for line12 in fi12:
#         singleurl12 = "http://" + line12.rstrip().replace('|','')
#         urls12['url'] = singleurl12
#         urls12['_id'] = tomd5(singleurl12)
#         decodedurl12 = urllib.parse.unquote(singleurl12) #把encode的url先decode
#         list12 = tldextract.extract(decodedurl12)
#         domain_name12 = list12.domain + '.' + list12.suffix
#         urls12['from'] = domain_name12
#         urls12['for'] = 'crawler12'
#         if urls12['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls12)
#             except:
#                 pass

# for file_name13 in list_of_files[49:52]:
#     fi13 = open(file_name13,"r")
#     urls13 = {}
#     for line13 in fi13:
#         singleurl13 = "http://" + line13.rstrip().replace('|','')
#         urls13['url'] = singleurl13
#         urls13['_id'] = tomd5(singleurl13)
#         decodedurl13 = urllib.parse.unquote(singleurl13) #把encode的url先decode
#         list13 = tldextract.extract(decodedurl13)
#         domain_name13 = list13.domain + '.' + list13.suffix
#         urls13['from'] = domain_name13
#         urls13['for'] = 'crawler13'
#         if urls13['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls13)
#             except:
#                 pass

# for file_name14 in list_of_files[53:56]:
#     fi14 = open(file_name14,"r")
#     urls14 = {}
#     for line14 in fi14:
#         singleurl14 = "http://" + line14.rstrip().replace('|','')
#         urls14['url'] = singleurl14
#         urls14['_id'] = tomd5(singleurl14)
#         decodedurl14 = urllib.parse.unquote(singleurl14) #把encode的url先decode
#         list14 = tldextract.extract(decodedurl14)
#         domain_name14 = list14.domain + '.' + list14.suffix
#         urls14['from'] = domain_name14
#         urls14['for'] = 'crawler14'
#         if urls14['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls14)
#             except:
#                 pass

# for file_name15 in list_of_files[57:60]:
#     fi15 = open(file_name15,"r")
#     urls15 = {}
#     for line15 in fi15:
#         singleurl15 = "http://" + line15.rstrip().replace('|','')
#         urls15['url'] = singleurl15
#         urls15['_id'] = tomd5(singleurl15)
#         decodedurl15 = urllib.parse.unquote(singleurl15) #把encode的url先decode
#         list15 = tldextract.extract(decodedurl15)
#         domain_name15 = list15.domain + '.' + list15.suffix
#         urls15['from'] = domain_name15
#         urls15['for'] = 'crawler15'
#         if urls15['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls15)
#             except:
#                 pass

# for file_name16 in list_of_files[61:64]:
#     fi16 = open(file_name16,"r")
#     urls16 = {}
#     for line16 in fi16:
#         singleurl16 = "http://" + line16.rstrip().replace('|','')
#         urls16['url'] = singleurl16
#         urls16['_id'] = tomd5(singleurl16)
#         decodedurl16 = urllib.parse.unquote(singleurl16) #把encode的url先decode
#         list16 = tldextract.extract(decodedurl16)
#         domain_name16 = list16.domain + '.' + list16.suffix
#         urls16['from'] = domain_name16
#         urls16['for'] = 'crawler16'
#         if urls16['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls16)
#             except:
#                 pass

# for file_name17 in list_of_files[65:68]:
#     fi17 = open(file_name17,"r")
#     urls17 = {}
#     for line17 in fi17:
#         singleurl17 = "http://" + line17.rstrip().replace('|','')
#         urls17['url'] = singleurl17
#         urls17['_id'] = tomd5(singleurl17)
#         decodedurl17 = urllib.parse.unquote(singleurl17) #把encode的url先decode
#         list17 = tldextract.extract(decodedurl17)
#         domain_name17 = list17.domain + '.' + list17.suffix
#         urls17['from'] = domain_name17
#         urls17['for'] = 'crawler17'
#         if urls17['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls17)
#             except:
#                 pass

# for file_name18 in list_of_files[69:72]:
#     fi18 = open(file_name18,"r")
#     urls18 = {}
#     for line18 in fi18:
#         singleurl18 = "http://" + line18.rstrip().replace('|','')
#         urls18['url'] = singleurl18
#         urls18['_id'] = tomd5(singleurl18)
#         decodedurl18 = urllib.parse.unquote(singleurl18) #把encode的url先decode
#         list18 = tldextract.extract(decodedurl18)
#         domain_name18 = list18.domain + '.' + list18.suffix
#         urls18['from'] = domain_name18
#         urls18['for'] = 'crawler18'
#         if urls18['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls18)
#             except:
#                 pass

# for file_name19 in list_of_files[73:76]:
#     fi19 = open(file_name19,"r")
#     urls19 = {}
#     for line19 in fi19:
#         singleurl19 = "http://" + line19.rstrip().replace('|','')
#         urls19['url'] = singleurl19
#         urls19['_id'] = tomd5(singleurl19)
#         decodedurl19 = urllib.parse.unquote(singleurl19) #把encode的url先decode
#         list19 = tldextract.extract(decodedurl19)
#         domain_name19 = list19.domain + '.' + list19.suffix
#         urls19['from'] = domain_name19
#         urls19['for'] = 'crawler19'
#         if urls19['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls19)
#             except:
#                 pass

# for file_name20 in list_of_files[77:80]:
#     fi20 = open(file_name20,"r")
#     urls20 = {}
#     for line20 in fi20:
#         singleurl20 = "http://" + line20.rstrip().replace('|','')
#         urls20['url'] = singleurl20
#         urls20['_id'] = tomd5(singleurl20)
#         decodedurl20 = urllib.parse.unquote(singleurl20) #把encode的url先decode
#         list20 = tldextract.extract(decodedurl20)
#         domain_name20 = list20.domain + '.' + list20.suffix
#         urls20['from'] = domain_name20
#         urls20['for'] = 'crawler20'
#         if urls20['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls20)
#             except:
#                 pass

# for file_name21 in list_of_files[81:84]:
#     fi21 = open(file_name21,"r")
#     urls21 = {}
#     for line21 in fi21:
#         singleurl21 = "http://" + line21.rstrip().replace('|','')
#         urls21['url'] = singleurl21
#         urls21['_id'] = tomd5(singleurl21)
#         decodedurl21 = urllib.parse.unquote(singleurl21) #把encode的url先decode
#         list21 = tldextract.extract(decodedurl21)
#         domain_name21 = list21.domain + '.' + list21.suffix
#         urls21['from'] = domain_name21
#         urls21['for'] = 'crawler21'
#         if urls21['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls21)
#             except:
#                 pass

# for file_name22 in list_of_files[85:88]:
#     fi22 = open(file_name22,"r")
#     urls22 = {}
#     for line22 in fi22:
#         singleurl22 = "http://" + line22.rstrip().replace('|','')
#         urls22['url'] = singleurl22
#         urls22['_id'] = tomd5(singleurl22)
#         decodedurl22 = urllib.parse.unquote(singleurl22) #把encode的url先decode
#         list22 = tldextract.extract(decodedurl22)
#         domain_name22 = list22.domain + '.' + list22.suffix
#         urls22['from'] = domain_name22
#         urls22['for'] = 'crawler22'
#         if urls22['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls22)
#             except:
#                 pass

# for file_name23 in list_of_files[89:92]:
#     fi23 = open(file_name23,"r")
#     urls23 = {}
#     for line23 in fi23:
#         singleurl23 = "http://" + line23.rstrip().replace('|','')
#         urls23['url'] = singleurl23
#         urls23['_id'] = tomd5(singleurl23)
#         decodedurl23 = urllib.parse.unquote(singleurl23) #把encode的url先decode
#         list23 = tldextract.extract(decodedurl23)
#         domain_name23 = list23.domain + '.' + list23.suffix
#         urls23['from'] = domain_name23
#         urls23['for'] = 'crawler23'
#         if urls23['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls23)
#             except:
#                 pass

# for file_name24 in list_of_files[93:96]:
#     fi24 = open(file_name24,"r")
#     urls24 = {}
#     for line24 in fi24:
#         singleurl24 = "http://" + line24.rstrip().replace('|','')
#         urls24['url'] = singleurl24
#         urls24['_id'] = tomd5(singleurl24)
#         decodedurl24 = urllib.parse.unquote(singleurl24) #把encode的url先decode
#         list24 = tldextract.extract(decodedurl24)
#         domain_name24 = list24.domain + '.' + list24.suffix
#         urls24['from'] = domain_name24
#         urls24['for'] = 'crawler24'
#         if urls24['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls24)
#             except:
#                 pass

# for file_name25 in list_of_files[97:100]:
#     fi25 = open(file_name25,"r")
#     urls25 = {}
#     for line25 in fi25:
#         singleurl25 = "http://" + line25.rstrip().replace('|','')
#         urls25['url'] = singleurl25
#         urls25['_id'] = tomd5(singleurl25)
#         decodedurl25 = urllib.parse.unquote(singleurl25) #把encode的url先decode
#         list25 = tldextract.extract(decodedurl25)
#         domain_name25 = list25.domain + '.' + list25.suffix
#         urls25['from'] = domain_name25
#         urls25['for'] = 'crawler25'
#         if urls25['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls25)
#             except:
#                 pass

# for file_name26 in list_of_files[101:104]:
#     fi26 = open(file_name26,"r")
#     urls26 = {}
#     for line26 in fi26:
#         singleurl26 = "http://" + line26.rstrip().replace('|','')
#         urls26['url'] = singleurl26
#         urls26['_id'] = tomd5(singleurl26)
#         decodedurl26 = urllib.parse.unquote(singleurl26) #把encode的url先decode
#         list26 = tldextract.extract(decodedurl26)
#         domain_name26 = list26.domain + '.' + list26.suffix
#         urls26['from'] = domain_name26
#         urls26['for'] = 'crawler26'
#         if urls26['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls26)
#             except:
#                 pass

# for file_name27 in list_of_files[105:108]:
#     fi27 = open(file_name27,"r")
#     urls27 = {}
#     for line27 in fi27:
#         singleurl27 = "http://" + line27.rstrip().replace('|','')
#         urls27['url'] = singleurl27
#         urls27['_id'] = tomd5(singleurl27)
#         decodedurl27 = urllib.parse.unquote(singleurl27) #把encode的url先decode
#         list27 = tldextract.extract(decodedurl27)
#         domain_name27 = list27.domain + '.' + list27.suffix
#         urls27['from'] = domain_name27
#         urls27['for'] = 'crawler27'
#         if urls27['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls27)
#             except:
#                 pass

# for file_name28 in list_of_files[109:112]:
#     fi28 = open(file_name28,"r")
#     urls28 = {}
#     for line28 in fi28:
#         singleurl28 = "http://" + line28.rstrip().replace('|','')
#         urls28['url'] = singleurl28
#         urls28['_id'] = tomd5(singleurl28)
#         decodedurl28 = urllib.parse.unquote(singleurl28) #把encode的url先decode
#         list28 = tldextract.extract(decodedurl28)
#         domain_name28 = list28.domain + '.' + list28.suffix
#         urls28['from'] = domain_name28
#         urls28['for'] = 'crawler28'
#         if urls28['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls28)
#             except:
#                 pass

# for file_name29 in list_of_files[113:116]:
#     fi29 = open(file_name29,"r")
#     urls29 = {}
#     for line29 in fi29:
#         singleurl29 = "http://" + line29.rstrip().replace('|','')
#         urls29['url'] = singleurl29
#         urls29['_id'] = tomd5(singleurl29)
#         decodedurl29 = urllib.parse.unquote(singleurl29) #把encode的url先decode
#         list29 = tldextract.extract(decodedurl29)
#         domain_name29 = list29.domain + '.' + list29.suffix
#         urls29['from'] = domain_name29
#         urls29['for'] = 'crawler29'
#         if urls29['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls29)
#             except:
#                 pass

# for file_name30 in list_of_files[117:120]:
#     fi30 = open(file_name30,"r")
#     urls30 = {}
#     for line30 in fi30:
#         singleurl30 = "http://" + line30.rstrip().replace('|','')
#         urls30['url'] = singleurl30
#         urls30['_id'] = tomd5(singleurl30)
#         decodedurl30 = urllib.parse.unquote(singleurl30) #把encode的url先decode
#         list30 = tldextract.extract(decodedurl30)
#         domain_name30 = list30.domain + '.' + list30.suffix
#         urls30['from'] = domain_name30
#         urls30['for'] = 'crawler30'
#         if urls30['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls30)
#             except:
#                 pass

# for file_name31 in list_of_files[121:124]:
#     fi31 = open(file_name31,"r")
#     urls31 = {}
#     for line31 in fi31:
#         singleurl31 = "http://" + line31.rstrip().replace('|','')
#         urls31['url'] = singleurl31
#         urls31['_id'] = tomd5(singleurl31)
#         decodedurl31 = urllib.parse.unquote(singleurl31) #把encode的url先decode
#         list31 = tldextract.extract(decodedurl31)
#         domain_name31 = list31.domain + '.' + list31.suffix
#         urls31['from'] = domain_name31
#         urls31['for'] = 'crawler31'
#         if urls31['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls31)
#             except:
#                 pass

# for file_name32 in list_of_files[125:128]:
#     fi32 = open(file_name32,"r")
#     urls32 = {}
#     for line32 in fi32:
#         singleurl32 = "http://" + line32.rstrip().replace('|','')
#         urls32['url'] = singleurl32
#         urls32['_id'] = tomd5(singleurl32)
#         decodedurl32 = urllib.parse.unquote(singleurl32) #把encode的url先decode
#         list32 = tldextract.extract(decodedurl32)
#         domain_name32 = list32.domain + '.' + list32.suffix
#         urls32['from'] = domain_name32
#         urls32['for'] = 'crawler32'
#         if urls32['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls32)
#             except:
#                 pass

# for file_name33 in list_of_files[129:132]:
#     fi33 = open(file_name33,"r")
#     urls33 = {}
#     for line33 in fi33:
#         singleurl33 = "http://" + line33.rstrip().replace('|','')
#         urls33['url'] = singleurl33
#         urls33['_id'] = tomd5(singleurl33)
#         decodedurl33 = urllib.parse.unquote(singleurl33) #把encode的url先decode
#         list33 = tldextract.extract(decodedurl33)
#         domain_name33 = list33.domain + '.' + list33.suffix
#         urls33['from'] = domain_name33
#         urls33['for'] = 'crawler33'
#         if urls33['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls33)
#             except:
#                 pass

# for file_name34 in list_of_files[133:136]:
#     fi34 = open(file_name34,"r")
#     urls34 = {}
#     for line34 in fi34:
#         singleurl34 = "http://" + line34.rstrip().replace('|','')
#         urls34['url'] = singleurl34
#         urls34['_id'] = tomd5(singleurl34)
#         decodedurl34 = urllib.parse.unquote(singleurl34) #把encode的url先decode
#         list34 = tldextract.extract(decodedurl34)
#         domain_name34 = list34.domain + '.' + list34.suffix
#         urls34['from'] = domain_name34
#         urls34['for'] = 'crawler34'
#         if urls34['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls34)
#             except:
#                 pass

# for file_name35 in list_of_files[137:140]:
#     fi35 = open(file_name35,"r")
#     urls35 = {}
#     for line35 in fi35:
#         singleurl35 = "http://" + line35.rstrip().replace('|','')
#         urls35['url'] = singleurl35
#         urls35['_id'] = tomd5(singleurl35)
#         decodedurl35 = urllib.parse.unquote(singleurl35) #把encode的url先decode
#         list35 = tldextract.extract(decodedurl35)
#         domain_name35 = list35.domain + '.' + list35.suffix
#         urls35['from'] = domain_name35
#         urls35['for'] = 'crawler35'
#         if urls35['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls35)
#             except:
#                 pass

# for file_name36 in list_of_files[141:144]:
#     fi36 = open(file_name36,"r")
#     urls36 = {}
#     for line36 in fi36:
#         singleurl36 = "http://" + line36.rstrip().replace('|','')
#         urls36['url'] = singleurl36
#         urls36['_id'] = tomd5(singleurl36)
#         decodedurl36 = urllib.parse.unquote(singleurl36) #把encode的url先decode
#         list36 = tldextract.extract(decodedurl36)
#         domain_name36 = list36.domain + '.' + list36.suffix
#         urls36['from'] = domain_name36
#         urls36['for'] = 'crawler36'
#         if urls36['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls36)
#             except:
#                 pass

# for file_name37 in list_of_files[145:148]:
#     fi37 = open(file_name37,"r")
#     urls37 = {}
#     for line37 in fi37:
#         singleurl37 = "http://" + line37.rstrip().replace('|','')
#         urls37['url'] = singleurl37
#         urls37['_id'] = tomd5(singleurl37)
#         decodedurl37 = urllib.parse.unquote(singleurl37) #把encode的url先decode
#         list37 = tldextract.extract(decodedurl37)
#         domain_name37 = list37.domain + '.' + list37.suffix
#         urls37['from'] = domain_name37
#         urls37['for'] = 'crawler37'
#         if urls37['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls37)
#             except:
#                 pass

# for file_name38 in list_of_files[149:152]:
#     fi38 = open(file_name38,"r")
#     urls38 = {}
#     for line38 in fi38:
#         singleurl38 = "http://" + line38.rstrip().replace('|','')
#         urls38['url'] = singleurl38
#         urls38['_id'] = tomd5(singleurl38)
#         decodedurl38 = urllib.parse.unquote(singleurl38) #把encode的url先decode
#         list38 = tldextract.extract(decodedurl38)
#         domain_name38 = list38.domain + '.' + list38.suffix
#         urls38['from'] = domain_name38
#         urls38['for'] = 'crawler38'
#         if urls38['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls38)
#             except:
#                 pass

# for file_name39 in list_of_files[153:156]:
#     fi39 = open(file_name39,"r")
#     urls39 = {}
#     for line39 in fi39:
#         singleurl39 = "http://" + line39.rstrip().replace('|','')
#         urls39['url'] = singleurl39
#         urls39['_id'] = tomd5(singleurl39)
#         decodedurl39 = urllib.parse.unquote(singleurl39) #把encode的url先decode
#         list39 = tldextract.extract(decodedurl39)
#         domain_name39 = list39.domain + '.' + list39.suffix
#         urls39['from'] = domain_name39
#         urls39['for'] = 'crawler39'
#         if urls39['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls39)
#             except:
#                 pass

# for file_name40 in list_of_files[157:160]:
#     fi40 = open(file_name40,"r")
#     urls40 = {}
#     for line40 in fi40:
#         singleurl40 = "http://" + line40.rstrip().replace('|','')
#         urls40['url'] = singleurl40
#         urls40['_id'] = tomd5(singleurl40)
#         decodedurl40 = urllib.parse.unquote(singleurl40) #把encode的url先decode
#         list40 = tldextract.extract(decodedurl40)
#         domain_name40 = list40.domain + '.' + list40.suffix
#         urls40['from'] = domain_name40
#         urls40['for'] = 'crawler40'
#         if urls40['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls40)
#             except:
#                 pass

# for file_name41 in list_of_files[161:164]:
#     fi41 = open(file_name41,"r")
#     urls41 = {}
#     for line41 in fi41:
#         singleurl41 = "http://" + line41.rstrip().replace('|','')
#         urls41['url'] = singleurl41
#         urls41['_id'] = tomd5(singleurl41)
#         decodedurl41 = urllib.parse.unquote(singleurl41) #把encode的url先decode
#         list41 = tldextract.extract(decodedurl41)
#         domain_name41 = list41.domain + '.' + list41.suffix
#         urls41['from'] = domain_name41
#         urls41['for'] = 'crawler41'
#         if urls41['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls41)
#             except:
#                 pass

# for file_name42 in list_of_files[165:168]:
#     fi42 = open(file_name42,"r")
#     urls42 = {}
#     for line42 in fi42:
#         singleurl42 = "http://" + line42.rstrip().replace('|','')
#         urls42['url'] = singleurl42
#         urls42['_id'] = tomd5(singleurl42)
#         decodedurl42 = urllib.parse.unquote(singleurl42) #把encode的url先decode
#         list42 = tldextract.extract(decodedurl42)
#         domain_name42 = list42.domain + '.' + list42.suffix
#         urls42['from'] = domain_name42
#         urls42['for'] = 'crawler42'
#         if urls42['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls42)
#             except:
#                 pass

# for file_name43 in list_of_files[169:172]:
#     fi43 = open(file_name43,"r")
#     urls43 = {}
#     for line43 in fi43:
#         singleurl43 = "http://" + line43.rstrip().replace('|','')
#         urls43['url'] = singleurl43
#         urls43['_id'] = tomd5(singleurl43)
#         decodedurl43 = urllib.parse.unquote(singleurl43) #把encode的url先decode
#         list43 = tldextract.extract(decodedurl43)
#         domain_name43 = list43.domain + '.' + list43.suffix
#         urls43['from'] = domain_name43
#         urls43['for'] = 'crawler43'
#         if urls43['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls43)
#             except:
#                 pass

# for file_name44 in list_of_files[173:176]:
#     fi44 = open(file_name44,"r")
#     urls44 = {}
#     for line44 in fi44:
#         singleurl44 = "http://" + line44.rstrip().replace('|','')
#         urls44['url'] = singleurl44
#         urls44['_id'] = tomd5(singleurl44)
#         decodedurl44 = urllib.parse.unquote(singleurl44) #把encode的url先decode
#         list44 = tldextract.extract(decodedurl44)
#         domain_name44 = list44.domain + '.' + list44.suffix
#         urls44['from'] = domain_name44
#         urls44['for'] = 'crawler44'
#         if urls44['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls44)
#             except:
#                 pass

# for file_name45 in list_of_files[177:180]:
#     fi45 = open(file_name45,"r")
#     urls45 = {}
#     for line45 in fi45:
#         singleurl45 = "http://" + line45.rstrip().replace('|','')
#         urls45['url'] = singleurl45
#         urls45['_id'] = tomd5(singleurl45)
#         decodedurl45 = urllib.parse.unquote(singleurl45) #把encode的url先decode
#         list45 = tldextract.extract(decodedurl45)
#         domain_name45 = list45.domain + '.' + list45.suffix
#         urls45['from'] = domain_name45
#         urls45['for'] = 'crawler45'
#         if urls45['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls45)
#             except:
#                 pass

# for file_name46 in list_of_files[181:184]:
#     fi46 = open(file_name46,"r")
#     urls46 = {}
#     for line46 in fi46:
#         singleurl46 = "http://" + line46.rstrip().replace('|','')
#         urls46['url'] = singleurl46
#         urls46['_id'] = tomd5(singleurl46)
#         decodedurl46 = urllib.parse.unquote(singleurl46) #把encode的url先decode
#         list46 = tldextract.extract(decodedurl46)
#         domain_name46 = list46.domain + '.' + list46.suffix
#         urls46['from'] = domain_name46
#         urls46['for'] = 'crawler46'
#         if urls46['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls46)
#             except:
#                 pass

# for file_name47 in list_of_files[185:188]:
#     fi47 = open(file_name47,"r")
#     urls47 = {}
#     for line47 in fi47:
#         singleurl47 = "http://" + line47.rstrip().replace('|','')
#         urls47['url'] = singleurl47
#         urls47['_id'] = tomd5(singleurl47)
#         decodedurl47 = urllib.parse.unquote(singleurl47) #把encode的url先decode
#         list47 = tldextract.extract(decodedurl47)
#         domain_name47 = list47.domain + '.' + list47.suffix
#         urls47['from'] = domain_name47
#         urls47['for'] = 'crawler47'
#         if urls47['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls47)
#             except:
#                 pass

# for file_name48 in list_of_files[189:192]:
#     fi48 = open(file_name48,"r")
#     urls48 = {}
#     for line48 in fi48:
#         singleurl48 = "http://" + line48.rstrip().replace('|','')
#         urls48['url'] = singleurl48
#         urls48['_id'] = tomd5(singleurl48)
#         decodedurl48 = urllib.parse.unquote(singleurl48) #把encode的url先decode
#         list48 = tldextract.extract(decodedurl48)
#         domain_name48 = list48.domain + '.' + list48.suffix
#         urls48['from'] = domain_name48
#         urls48['for'] = 'crawler48'
#         if urls48['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls48)
#             except:
#                 pass

# for file_name49 in list_of_files[193:196]:
#     fi49 = open(file_name49,"r")
#     urls49 = {}
#     for line49 in fi49:
#         singleurl49 = "http://" + line49.rstrip().replace('|','')
#         urls49['url'] = singleurl49
#         urls49['_id'] = tomd5(singleurl49)
#         decodedurl49 = urllib.parse.unquote(singleurl49) #把encode的url先decode
#         list49 = tldextract.extract(decodedurl49)
#         domain_name49 = list49.domain + '.' + list49.suffix
#         urls49['from'] = domain_name49
#         urls49['for'] = 'crawler49'
#         if urls49['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls49)
#             except:
#                 pass

# for file_name50 in list_of_files[197:200]:
#     fi50 = open(file_name50,"r")
#     urls50 = {}
#     for line50 in fi50:
#         singleurl50 = "http://" + line50.rstrip().replace('|','')
#         urls50['url'] = singleurl50
#         urls50['_id'] = tomd5(singleurl50)
#         decodedurl50 = urllib.parse.unquote(singleurl50) #把encode的url先decode
#         list50 = tldextract.extract(decodedurl50)
#         domain_name50 = list50.domain + '.' + list50.suffix
#         urls50['from'] = domain_name50
#         urls50['for'] = 'crawler50'
#         if urls50['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls50)
#             except:
#                 pass

# for file_name51 in list_of_files[201:204]:
#     fi51 = open(file_name51,"r")
#     urls51 = {}
#     for line51 in fi51:
#         singleurl51 = "http://" + line51.rstrip().replace('|','')
#         urls51['url'] = singleurl51
#         urls51['_id'] = tomd5(singleurl51)
#         decodedurl51 = urllib.parse.unquote(singleurl51) #把encode的url先decode
#         list51 = tldextract.extract(decodedurl51)
#         domain_name51 = list51.domain + '.' + list51.suffix
#         urls51['from'] = domain_name51
#         urls51['for'] = 'crawler51'
#         if urls51['from'] in unwanted:
#             pass
#         else:
#             try:
#                 collection.insert_one(urls51)
#             except:
#                 pass