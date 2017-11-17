#這支程式用以判斷由DSP送來的url是否已存在在人群分類DB裏頭，並決定是否要將url送入url list DB待爬
# import newspaper
import hashlib
import time
import pymongo
from pymongo import MongoClient
try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['crawledurlsTest'] #dsp送過來的url
    collection2 = db['crawledurlsTest2'] # url list DB
    collection3 = db['temp2'] #人群標籤DB
    print("Connects to MongoDB successfully!!")
except:
    print('Cannot connect to MongoDB server!!')

#def encodeUrl(url):
#    hash_object = hashlib.md5(url.encode())
#    MD5code = hash_object.hexdigest()
#    url = {}
#    url['url'] = url
#    url['_id'] = MD5code
#    print(url)
#    return url
#encodeUrl("http://eznewlife.com/150535/以前都考100分？兒子竟意外翻出「爸爸的國中考卷」猛一看…網友都要跪惹！")
"""urls = []
documents = collection3.find()
for document in documents:
    mdid = document["_id"]
    urls.append(mdid)
#encodeUrl("https://www.soft4fun.net/tech/news/htc-u11-plus.htm")
#利用無窮迴圈，先設定每2分鐘訪問要抓url的網站一次，之後可以再做調整。
while True: #time.sleep(120)
    documents = collection.find()
    for document in documents:
        if document["_id"] not in urls:
            try:
                collection2.insert_one(document)
            except:
                pass
                print("nope")
            print("url sent to list DB")
        else:
            print("url already exists")
    time.sleep(120)"""
