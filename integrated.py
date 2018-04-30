#這支程式專門跑 url list DB裏頭的url，轉成文章分析內容(content,TFIDF,unixtime...等等)
# import jieba
# import jieba.analyse
from operator import itemgetter as i
from functools import cmp_to_key
import urllib.parse
import operator
import re
import newspaper
from newspaper import Article
import time
# from datetime import datetime
import hashlib
import math
#import redis
import pymongo
from pymongo import MongoClient
try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['dict'] #這是DSP曝光url待爬中的
    # collection2 = db['interestgroups'] #這是我們自己要保存得拿來訓練模型
    # collection3 = db['to_redis'] #這是要push給仁邑的Redis
except:
    print('Cannot connect to MongoDB server!!')
#--------------------------------------------------------------------------------------------
# collection3.create_index([("createdDatetime", 1)], expireAfterSeconds=691200) #8天過期
def getArticle(url):
    art_dict = {} #把文章內容存成一個 dictionary
    decodedurl = urllib.parse.unquote(url)
    art = Article(decodedurl, language = "zh")
    try:
        art.download() #載入文章
        art.parse() #從文字上分析
    except:
        print('cannot download texts!!')
        pass
    art_text = art.text.replace('\n', '').replace('\'', '').replace('\"', '').replace("\xa0", "").replace("\u3000", "").replace("\xa06", "").replace("\xa03", "").replace("\xa02", "").replace("\xa01", "").strip()
    art_url = art.url.replace   ("\n", "")   #原始的url
    unixtime = int(time.time())  #標記時間戳(系統時間)
    hash_object = hashlib.md5(art_url.encode())
    MD5code = hash_object.hexdigest()  #將url轉成MD5並且存取下來
    # jieba.set_dictionary('C:\\Users\\defaultuser0\\dict.txt')  #結巴斷詞字庫
    # words = jieba.cut(art_text, cut_all=False)
    # words = jieba.analyse.set_stop_words('C:\\Users\\defaultuser0\\stopwords(ken).txt')
    # words = jieba.analyse.extract_tags(str(re.sub("[0-9]", "", art_text)),15)  #利用jieba.analyse來計算文本TF-IDF關鍵詞
    art_dict["content"] = art_text         #switch to match
    art_dict["url"] = decodedurl
    # art_dict["unix_time"] = unixtime
    art_dict["_id"] = MD5code
    # art_dict["TF-IDF words list"] = str(words).replace("[", "").replace("]", "")
    return art_dict #記得換回art_dict

# print("start extracting words")
# start = time.time()
# end = time.time()
# elapsed = end - start
# print('finished')
# print ("Time taken: ", elapsed, "seconds.")
#---------------------------------------------------------------------------------------------
print("start extracting words")
start = time.time()
art_words = getArticle('https://www.fe-amart.com.tw/index.php/life-style/life-info/secret-recipe/hero-6')['content']
documents = collection.find()
wd_weight = []
for d in documents:
    if d['_id'] in art_words and int(len(d['_id']) > int(1)):
        wd_count = {}
        wd_count['count'] = art_words.count(d['_id']) #在這篇文章出現幾次 int型態
        wd_count['word'] = d['_id']
        wd_count['weight'] = (math.log10(wd_count['count']+0)*math.log10(len(d['_id'])+3)) / math.log10(int(d['hours_count'])+100)
        wd_weight.append(wd_count)

def cmp(a, b):
    return (a > b) - (a < b)
def multikeysort(items, columns):
    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith('-') else (i(col.strip()), 1))
        for col in columns
    ]
    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))

ass = multikeysort(wd_weight, ['-weight','word'])
for a in ass[:10]:
    print(a['word'])
end = time.time()
elapsed = end - start
print('finished')
print ("Time taken: ", elapsed, "seconds.")
