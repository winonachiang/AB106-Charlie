import os
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
    client = MongoClient('127.0.0.1', 27017) 
    db = client['dsp_url'] #連結到mongoDB裡的database
    # to_redis = db['test_urls_o'] #這是DSP曝光url待爬中的
    collection = db['test_urls'] #這是DSP曝光url待爬中的
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
            try:
                collection.insert_one(urls)
            except:
                pass

os.system("python3 /home/c29559810/s3/send.py")

end = time.time()
elapsed = end - start
print('all sent')
print ("Time taken: ", elapsed, "seconds.")
