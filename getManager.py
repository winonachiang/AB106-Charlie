#寫個log把程式執行的動作記錄起來
#取得與mongoDB的連線
import jieba
import jieba.analyse
from newspaper import Article
import time
import hashlib
import newspaper
import re
#re_words = re.compile("[\u4e00-\u9fa5]+")
import pymongo
from pymongo import MongoClient
try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['temp'] #連結到該database的table
    #collection2 = db['temp2']
    print("Connects to MongoDB successfully!!")
except:
    print('Cannot connect to MongoDB server!')
#
#---------------------------------------------我是分隔線----------------------------------------------

#Get contents of articles and insert them into mongoDB
#Main program:
"""def getArticle(url):
    art_dict = {} #把文章內容存成一個 dictionary
    art = Article(url, language = "zh")
    try:
        art.download() #載入文章
        art.parse() #從文字上分析
    except:
        print('cannot download texts!!')
        pass
    art_text = art.text.replace('\n', '').replace('\'', '').replace('\"', '').replace("\xa0", "").replace("\u3000", "").replace("\xa06", "").replace("\xa03", "").replace("\xa02", "").replace("\xa01", "").strip()
    art_url = art.url.replace("\n", "")   #原始的url
    unixtime = int(time.time())  #標記時間戳(系統時間)
    hash_object = hashlib.md5(art_url.encode())
    MD5code = hash_object.hexdigest()  #將url轉成MD5並且存取下來
    #match = re.findall(re_words, art_text)
    jieba.set_dictionary('C:\\Users\\defaultuser0\\dict.txt')  #結巴斷詞字庫
    words = jieba.cut(art_text, cut_all=False)
    words = jieba.analyse.set_stop_words('C:\\Users\\defaultuser0\\stopwords(ken).txt')
    words = jieba.analyse.extract_tags(str(re.sub("[0-9]", "", art_text)),15)  #利用jieba.analyse來計算文本TF-IDF關鍵詞
    art_dict["content"] = art_text         #switch to match
    art_dict["url"] = art_url
    #art_dict["source"] = "technews"
    art_dict["unix_time"] = unixtime
    art_dict["_id"] = MD5code
    art_dict["TF-IDF words list"] = str(words).replace("[", "").replace("]", "")
    print(art_dict)
    return art_dict #記得換回art_dict"""
#
#getArticle("http://www.autonet.com.tw/cgi-bin/view.cgi?/news/2017/10/b7100253.ti+a2+a3+a4+a5+b1+/news/2017/10/b7100253+/news/2017/10/20+b3+d6+c1+c2+c3+e1+e2+e3+e5+f1")
#-----------------------------------------------------------------------------------------------------
#
#documents = collection2.find()
"""for document in documents:
    try:
        keywords = getArticle(document['url'])
        if len(keywords['content']) > 130:
            collection2.insert_one(keywords)
            #collection.delete_one({"unixtime":{"$exists":False}})
        else:
            print("This article is too short.")
            pass
        #print(keywords)
    except:
        print("http 404 not found!")
        pass"""
#for document in documents:
    #print(document["_id"])
    #print(document["TF-IDF words list"].replace("'","").replace(",",""))
#-----------------------------------------------------------------------------------------------------
"""import csv
with open("C:\\Users\\USER\\Documents\\ID(test).csv") as csvfile:
    spamreader = csv.DictReader(csvfile)
    #topics = {}
    for row in spamreader:
        topic = row['topics']
        print(topic)
        collection.find_one_and_update({'topics':{'$exists':False}},{"$set":{"topics":topic}}, upsert=True)"""
#
"""from collections import Counter
with open("C:\\Users\\USER\\Desktop\\charlie-stopwords.txt", "r", encoding="utf8") as f:
    words = f.readlines()

word_cnt = Counter()
for word in words:
    if word in word_cnt:
        word_cnt[word] += 1
    else:
        word_cnt[word] = 1
print(word_cnt.most_common())"""
