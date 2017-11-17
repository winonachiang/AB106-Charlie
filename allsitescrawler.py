from newspaper import Article
import time
import hashlib
import newspaper
import pymongo
from pymongo import MongoClient
try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['crawledurlsTest'] #連結到該database的table
    #collection2 = db['crawledurlsTest2']
    print("Connects to MongoDB successfully!!")
except:
    print('Cannot connect to MongoDB server!')

def insertUrl(url):
    hash_object = hashlib.md5(url.encode())
    MD5code = hash_object.hexdigest()
    urls = {}
    urls['url'] = url
    urls['_id'] = MD5code
    return urls


#利用無窮迴圈，先設定每2分鐘訪問要抓url的網站一次，之後可以再做調整。
while True: #time.sleep(120)
	#東森新聞                                            #後面參數要取消掉重複爬url的功能
    print("scrapying ettoday")
    ettoday = newspaper.build("https://www.ettoday.net/", memoize_articles=False)
    for article in ettoday.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #中央通訊社
    print("scrapying cna")
    cna = newspaper.build("http://www.cna.com.tw/", memoize_articles=False)
    for article in cna.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #pchome新聞網
    print("scrapying pchome")
    pchome = newspaper.build("http://news.pchome.com.tw/", memoize_articles=False)
    for article in pchome.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #聯合新聞網
    print("scrapying udn")
    udn = newspaper.build("https://udn.com/news/index", memoize_articles=False)
    for article in udn.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #三立新聞網
    print("scrapying set tv")
    setn = newspaper.build("http://www.setn.com/", memoize_articles=False)
    for article in setn.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #自由時報
    print("scrapying liberty news")
    ltn = newspaper.build("http://www.ltn.com.tw/", memoize_articles=False)
    for article in ltn.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #蘋果日報
    print("scrapying appledaily")
    appledaily = newspaper.build("https://tw.appledaily.com/", memoize_articles=False)
    for article in appledaily.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #新頭殼
    print("scrapying newtalk")
    newtalk = newspaper.build("https://newtalk.tw/", memoize_articles=False)
    for article in newtalk.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #今日新聞
    print("scrapying nownews")
    nownews = newspaper.build("https://www.nownews.com/", memoize_articles=False)
    for article in nownews.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #端傳媒
    print("scrapying theinitium")
    theinitium = newspaper.build("https://theinitium.com/", memoize_articles=False)
    for article in theinitium.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #報導者
    print("scrapying twreporter")
    twreporter = newspaper.build("https://www.twreporter.org/", memoize_articles=False)
    for article in twreporter.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #蘋果日報-體育
    print("scrapying apple sports")
    applesports = newspaper.build("https://tw.sports.appledaily.com/daily/", memoize_articles=False)
    for article in applesports.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #移人
    print("scrapying mpark")
    mpark = newspaper.build("http://mpark.news/", memoize_articles=False)
    for article in mpark.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #女人迷
    print("scrapying womany")
    womany = newspaper.build("https://womany.net/", memoize_articles=False)
    for article in womany.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #閱讀最前線
    print("scrapying readmoo")
    readmoo = newspaper.build("https://news.readmoo.com/", memoize_articles=False)
    for article in readmoo.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #痞客邦(所有旅遊)
    print("scrapying pixnettravel")
    pixnettravel = newspaper.build("https://travel.pixnet.net/", memoize_articles=False)
    for article in pixnettravel.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #buzzlife生活網
    print("scrapying buzzlife")
    buzzlife = newspaper.build("http://buzzlife.com.tw/", memoize_articles=False)
    for article in buzzlife.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #華人健康網
    print("scrapying tophealth")
    tophealth = newspaper.build("https://www.top1health.com/", memoize_articles=False)
    for article in tophealth.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #ifashion瘋時尚
    print("scrapying ifashion")
    ifashion = newspaper.build("http://ifashiontrend.com/", memoize_articles=False)
    for article in ifashion.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #vogue時尚網
    print("scrapying vogue")
    vogue = newspaper.build("https://www.vogue.com.tw/", memoize_articles=False)
    for article in vogue.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #techbang T客邦
    print("scrapying techbang")
    techbang = newspaper.build("https://www.techbang.com/", memoize_articles=False)
    for article in techbang.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #科技報橘
    print("scrapying buzzorange")
    buzzorange = newspaper.build("https://buzzorange.com/techorange/", memoize_articles=False)
    for article in buzzorange.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #科技新報
    print("scrapying technews")
    technews = newspaper.build("https://technews.tw/", memoize_articles=False)
    for article in technews.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #硬是要學
    print("scrapying soft4fun")
    soft4fun = newspaper.build("https://www.soft4fun.net/", memoize_articles=False)
    for article in soft4fun.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #engadget中文版
    print("scrapying engadget")
    engadget = newspaper.build("https://chinese.engadget.com/", memoize_articles=False)
    for article in engadget.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #bnext數位時代
    print("scrapying bnext")
    bnext = newspaper.build("https://www.bnext.com.tw/", memoize_articles=False)
    for article in bnext.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #mr.market市場先生
    print("scrapying rich01")
    rich01 = newspaper.build("http://www.rich01.com/", memoize_articles=False)
    for article in rich01.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #moneydj理財網
    print("scrapying moneydj")
    moneydj = newspaper.build("https://www.moneydj.com/", memoize_articles=False)
    for article in moneydj.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #社企流seinsights
    print("scrapying seinsights")
    seinsights = newspaper.build("http://www.seinsights.asia/", memoize_articles=False)
    for article in seinsights.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #天下雜誌
    print("scrapying cw")
    cw = newspaper.build("http://www.cw.com.tw/", memoize_articles=False)
    for article in cw.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #buycartv
    print("scrapying buycartv")
    buycartv = newspaper.build("https://www.buycartv.com/", memoize_articles=False)
    for article in buycartv.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #autonet汽車日報
    print("scrapying autonet")
    autonet = newspaper.build("http://www.autonet.com.tw/cgi-bin/view.cgi?a1+a2-i+a3+a4+a5+b1+b2+b3+c1+c2+c3+c4+d1+d2+d3+d4+d5+e1-i+e2+e3+e4+e5+f1", memoize_articles=False)
    for article in autonet.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #moto7
    print("scrapying moto7")
    moto7 = newspaper.build("https://www.moto7.net/", memoize_articles=False)
    for article in moto7.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #babynews育兒新知
    print("scrapying babynews")
    babynews = newspaper.build("http://babynews.in-mommy.com/", memoize_articles=False)
    for article in babynews.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #gamebase遊戲基地
    print("scrapying gamebase")
    gamebase = newspaper.build("https://www.gamebase.com.tw/", memoize_articles=False)
    for article in gamebase.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #digiphoto
    print("scrapying digiphoto")
    digiphoto = newspaper.build("https://digiphoto.techbang.com/", memoize_articles=False)
    for article in digiphoto.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #cookpad
    print("scrapying cookpad")
    cookpad = newspaper.build("https://cookpad.com/tw", memoize_articles=False)
    for article in cookpad.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #韓娛最前線
    print("scrapying kpopn")
    kpopn = newspaper.build("https://www.kpopn.com/", memoize_articles=False)
    for article in kpopn.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #麗臺運動報
    print("scrapying ltsports")
    ltsports = newspaper.build("https://www.ltsports.com.tw/", memoize_articles=False)
    for article in ltsports.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #動網dongtw
    print("scrapying dongtw")
    dongtw = newspaper.build("http://www.dongtw.com/", memoize_articles=False)
    for article in dongtw.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #大人物
    print("scrapying damanwoo")
    damanwoo = newspaper.build("https://www.damanwoo.com/", memoize_articles=False)
    for article in damanwoo.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #open design室內設計
    print("scrapying openworld")
    openworld = newspaper.build("http://openworld.tv/", memoize_articles=False)
    for article in openworld.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #黑秀heyshow
    print("scrapying heyshow")
    heyshow = newspaper.build("http://www.heyshow.com/", memoize_articles=False)
    for article in heyshow.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #愛寵物ipetgroup
    print("scrapying ipetgroup")
    ipetgroup = newspaper.build("https://ipetgroup.com/", memoize_articles=False)
    for article in ipetgroup.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)
    #網路溫度計dailyview
    print("scrapying dailyview")
    dailyview = newspaper.build("https://dailyview.tw/", memoize_articles=False)
    for article in dailyview.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            pass
    time.sleep(10)