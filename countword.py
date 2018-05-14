import time
t = time.time()
from datetime import datetime
import pymongo
from pymongo import MongoClient
from collections import Counter
try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['tagwords']
    collection2 = db['tagwords_hour']
except:
    print('Cannot connect to MongoDB server!!')

wordslist = []
documents = collection.find()
for d in documents:
    wordslist.append(d['word'])

word_cnt = Counter()
for word in wordslist:
    if word in word_cnt:
        word_cnt[word] += 1
    else:
        word_cnt[word] = 1

count_result = word_cnt.most_common()

for c in count_result:
    if c[1] > 1: #看出現在幾個網站，如果超過1個就把這個字計入到useful_word
        useful_word = {}
        useful_word['_id'] = c[0]
        useful_word['max_count'] = c[1]
        useful_word['stored_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        useful_word['modified_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        useful_word['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        try:
            collection2.insert_one(useful_word)
        except:
            collection2.update_one({'_id':useful_word['_id']},{'$set':{'mtime':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))}})
            original_hour = collection2.find_one({'_id':useful_word['_id']})
            if useful_word['max_count'] > original_hour['max_count']: # 判斷新的出現網站總計是否高於現在的出現網站總計
                collection2.update_one({'_id':useful_word['_id']},{'$set':{'max_count':useful_word['max_count'],'modified_time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))}})# 有高過就取代

#這裡是每個小時更新每個字詞出現的時間總計
def update_word(collection2):
    collection2.update_many({},{'$inc': {'hours_count':1}}, upsert=True)
update_word(collection2)

# documents = collection2.find()
# for d in documents:
#     collection2.update_many({},{'$set':{'mtime':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))}})
