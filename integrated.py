#這支程式專門跑 url list DB裏頭的url，轉成文章分析內容(content,TFIDF,unixtime...等等)
"""import jieba
import jieba.analyse
import re
import newspaper
from newspaper import Article
import time
import hashlib
import pymongo
from pymongo import MongoClient
try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['urllistDB'] #連結到待爬url的 urllistDB
    collection2 = db['interestgroups'] #把分析結果存入人群標籤DB-interestgroups
    print("Connects to MongoDB successfully!!")
except:
    print('Cannot connect to MongoDB server!!')"""

#--------------------------------------------------------------------------------------------
#
"""def getArticle(url):
    art_dict = {} #把文章內容存成一個 dictionary
    art = Article(url, language = "zh")
    try:
        art.download() #載入文章
        art.parse() #從文字上分析
    except:
        print('cannot download texts!!')
        pass #
    art_text = art.text.replace('\n', '').replace('\'', '').replace('\"', '').replace("\xa0", "").replace("\u3000", "").replace("\xa06", "").replace("\xa03", "").replace("\xa02", "").replace("\xa01", "").strip()
    art_url = art.url.replace("\n", "")   #原始的url
    unixtime = int(time.time())  #標記時間戳(系統時間)
    hash_object = hashlib.md5(art_url.encode())
    MD5code = hash_object.hexdigest()  #將url轉成MD5並且存取下來
    jieba.set_dictionary('C:\\Users\\defaultuser0\\dict.txt')  #結巴斷詞字庫
    words = jieba.cut(art_text, cut_all=False)
    words = jieba.analyse.set_stop_words('C:\\Users\\defaultuser0\\stopwords.txt')
    words = jieba.analyse.extract_tags(str(re.sub("[0-9]", "", art_text)),15)  #利用jieba.analyse來計算文本TF-IDF關鍵詞
    art_dict["content"] = art_text         #switch to match
    art_dict["url"] = art_url
    art_dict["unix_time"] = unixtime
    art_dict["_id"] = MD5code
    art_dict["TF-IDF words list"] = str(words).replace("[", "").replace("]", "")
    #print(art_dict)
    return art_dict #記得換回art_dict"""
#
#---------------------------------------------------------------------------------------------
#
"""while True:
    try:
        documents = collection.find()
        for document in documents:
            try:
                keywords = getArticle(document['url'])
                if len(keywords['content']) < 130:
                    print("This article is too short.")
                    pass
                else:
                    collection2.insert_one(keywords)
                collection.delete_one({"unixtime":{"$exists":False}})
            except:
                print("No urls found!")
                pass
    except:
        print("Cache is empty.")
    time.sleep(20)"""
