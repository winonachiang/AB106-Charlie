import sys
sys.path.append("C:\\Users\\USER")
import jieba
import jieba.analyse
from newspaper import Article
from urllib.request import urlopen
import time
import hashlib
import pymongo
from pymongo import MongoClient
try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['integrated'] #連結到該database的table
    print("Connects to MongoDB successfully!!")
except:
    print('Cannot connect to MongoDB server!!')
#url = collection.find_one({},{'_id':0})["url"] #將已經在資料庫裏頭的url宣告成全域變數，讓各function都讀得到
#----------------------------------------------------我是分隔線------------------------------------------------------
#1_url.py
#This step is to compile url into MD5 code and retrieve unixtime.
def getUnixtime():                                                                                                                                                                                                                       
    unixtime = int(time.time())  #標記時間戳(系統時間)
    return unixtime

def getMd5(url):
    hash_object = hashlib.md5(url.encode())
    MD5code = hash_object.hexdigest()  #將url轉成MD5並且存取下來
    return MD5code

try:
    url = collection.find_one({},{'_id':0})["url"]
    unixtime = getUnixtime()
    md5 = getMd5(url)
    db.integrated.update_one({},{"$set":{"MD5":md5}}) #insert MD5code into MongoDB
    db.integrated.update_one({},{"$set":{"unix_time":unixtime}}) #insert unixtime into MongoDB    
    print("Complied url successfully!")
except:
    print("Didn't connect to anything.")
    pass
#----------------------------------------------------我是分隔線------------------------------------------------------
#2_content.py
#This step is to get the cleared texts from an url.
def getContent(url):
    art = Article(url, language = "zh")
    try:
        art.download() #載入文章
        art.parse() 
    except:
        print('cannot download texts!!')
        pass
    art_text = art.text.replace('\n', '').replace('\'', '').replace('\"', '').replace("\xa0", "").replace("\u3000", "").replace("\xa06", "").replace("\xa03", "").replace("\xa02", "").replace("\xa01", "").strip()#word_cnt.most_common()[:10]                                                                                                                                                                                                                                                                
    #print(art_text)
    return art_text
#url = collection.find_one({},{'_id':0})["url"]
try:
    url = collection.find_one({},{'_id':0})["url"]
    artContent= getContent(url)
    collection.update_one({},{"$set":{"content":artContent}}) #insert into MongoDB
    print("Inserted the content successfully!!")
except:
    print("Unable to insert the content!")
#----------------------------------------------------我是分隔線------------------------------------------------------
#3_keywords.py
#This step is to calculate the keywords of an article.
def jiebaAnalysis(content):
    #result = collection.find_one({},["content"])
    jieba.set_dictionary('c:\\users\\defaultuser0\\dict.txt') #結巴斷詞字庫
    words = jieba.cut(content, cut_all=False)
    words = jieba.analyse.set_stop_words('C:\\Users\\defaultuser0\\stopwords.txt') #中文停用詞字庫
    words = jieba.analyse.extract_tags(str(content),10) #利用jieba.analyse來計算文本TF-IDF關鍵詞
    return words
    #collection.update_one({},{"$set":{"TD-IDF":str(words).replace("[", "").replace("]", "").replace("'", "")}}) 

try:
    content = collection.find_one({},["content"])
    tfidf = jiebaAnalysis(content)
    collection.update_one({},{"$set":{"TD-IDF":str(tfidf).replace("[", "").replace("]", "").replace("'", "")}})
    print("Successful analysis!!")
except: 
    print("Unable to analyze the text!!")