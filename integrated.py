#這支程式專門跑 url list DB裏頭的url，轉成文章分析內容(content,TFIDF,unixtime...等等)
from operator import itemgetter as i
from functools import cmp_to_key
import urllib.parse
import operator
import re
import newspaper
from newspaper import Article
import time
t = time.time()
from datetime import datetime
import hashlib
import math
import redis
import pymongo
from pymongo import MongoClient
try:
    client = MongoClient('10.140.0.7', 27017) #10.140.0.7
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['dict'] #這是DSP曝光url待爬中的
    db2 = client['dsp_url']
    # collection2 = db2['newcrawler01']
    # collection3 = db2['newcrawler02']
    # collection4 = db2['newcrawler03']
    # collection5 = db2['newcrawler04']
    # collection6 = db2['newcrawler05']
    # collection7 = db2['newcrawler06']
    # collection8 = db2['newcrawler07']
    # collection9 = db2['newcrawler08']
    # collection10 = db2['newcrawler09']
    # collection11 = db2['newcrawler10']
    # collection12 = db2['newcrawler11']
    # collection13 = db2['newcrawler12']
    # collection14 = db2['newcrawler13']
    # collection15 = db2['newcrawler14']
    # collection16 = db2['newcrawler15']
    # collection17 = db2['newcrawler16']
    # collection18 = db2['newcrawler17']
    # collection19 = db2['newcrawler18']
    # collection20 = db2['newcrawler19']
    collection21 = db2['newcrawler20']
    coll_redis = db2['to_redis'] #這是要push給仁邑的Redis
    # collection2 = db['interestgroups'] #這是我們自己要保存得拿來訓練模型
except:
    print('Cannot connect to MongoDB server!!')
#--------------------------------------------------------------------------------------------
# collection3.create_index([("createdDatetime", 1)], expireAfterSeconds=691200) #8天過期
def cmp(a, b): #比較權重dictionaries裏頭的值
    return (a > b) - (a < b)

def multikeysort(items, columns): #比較權重dictionaries裏頭的值
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1))
        for col in columns
    ]
    def comparer(left, right): #比較權重dictionaries裏頭的值
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))

def getArticle(url):
    art_dict = {} #把文章內容存成一個 dictionary
    decodedurl = urllib.parse.unquote(url) #把encode的url先decode
    art = Article(decodedurl, language = "zh")
    try:
        art.download() #載入文章
        art.parse()
    except:
        print('cannot download texts!!')
        pass
    art_text = art.text.replace('\n', '').replace('\'', '').replace('\"', '').replace("\xa0", "").replace("\u3000", "").replace("\xa06", "").replace("\xa03", "").replace("\xa02", "").replace("\xa01", "").strip()
    art_url = art.url.replace   ("\n", "")   #原始的url
    unixtime = int(time.time())  #標記時間戳(系統時間)
    hash_object = hashlib.md5(art_url.encode())
    MD5code = hash_object.hexdigest()  #將url轉成MD5並且存取下來
    wd_weight = [] #所有字的權重裝成一個list
    dictwords = collection.find() #讀取dict裏頭的字
    for d in dictwords: #比對dict裏頭的字
        if d['_id'] in art_text and int(len(d['_id']) > int(1)):
            wd_count = {}
            wd_count['count'] = art_text.count(d['_id']) #在這篇文章出現幾次 int型態
            wd_count['word'] = d['_id']
            wd_count['weight'] = (math.log10(wd_count['count']+0)*math.log10(len(d['_id'])+3)) / math.log10(int(d['hours_count'])+100)
            wd_weight.append(wd_count)
    wds_seq = multikeysort(wd_weight, ['-weight','word']) #排序關鍵字，由權重高到低
    wds_seq_list = []
    for w in wds_seq[:10]:
        wds_seq_list.append(w['word'])
    art_dict['keywords'] = str(wds_seq_list).replace('[','').replace(']','').replace("'","").replace(" ","")
    art_dict["content"] = art_text
    art_dict["url"] = decodedurl
    art_dict["unix_time"] = unixtime
    art_dict["_id"] = MD5code
    art_dict['stored_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
    art_dict['modified_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
    return art_dict #記得換回art_dict

#---------------------------------------------------------------------------------------------
print("start extracting words")
start = time.time()
c2s = collection21.find()#[:100] #帶爬的url的collection
for c2 in c2s:
    try:
        processed = getArticle(c2['url'])
        if len(processed['content']) > 50:
            try:
                coll_redis.insert_one(processed)
            except:
                coll_redis.update_one({'_id':processed['_id']},{'$set':{'modified_time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))}})
        else:
            pass
    except:
        pass
    collection21.delete_one({'_id':c2['_id']})
end = time.time()
elapsed = end - start
print('finished')
print ("Time taken: ", elapsed, "seconds.")
