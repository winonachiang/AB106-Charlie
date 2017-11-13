import newspaper
import hashlib
import time
import pymongo
from pymongo import MongoClient
try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['crawledurlsTest'] #連結到該database的table
    collection2 = db['crawledurlsTest2']
    print("Connects to MongoDB successfully!!")
except:
    print('Cannot connect to MongoDB server!!')

def insertUrl(url):
    hash_object = hashlib.md5(url.encode())
    MD5code = hash_object.hexdigest()
    urls = {}
    urls['url'] = url
    urls['_id'] = MD5code
    return urls
#利用無窮迴圈，先設定每2分鐘訪問要抓url的網站一次，之後可以再做調整。
while True: #time.sleep(120)                                 #後面參數要取消掉重複爬url的功能
    motorworld = newspaper.build("https://travel.pixnet.net/",  memoize_articles=False)
    for article in motorworld.articles:
        try:
            urlcompiled = insertUrl(article.url)
            collection.insert_one(urlcompiled)
        except:
            print("Unable to insert url!")
            pass
        print(article.url)
    time.sleep(120)

#url儲存資料庫DB-------------------------------------------------------------------------------------
newurl = {}
url = ""
hash_object = hashlib.md5(url.encode())
MD5code = hash_object.hexdigest()
newurl["_id"] = MD5code
newurl["url"] = url
#print(newurl["_id"])

urls = []
documents = collection.find()
for document in documents:
    mdid = document["_id"]
    urls.append(mdid)

if newurl["_id"] not in urls:
    collection2.insert_one(newurl)
    print("url is sent to list DB")
else:
    print("url already exists")
