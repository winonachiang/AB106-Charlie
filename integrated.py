#import jieba
#import jieba.analyse
#from newspaper import Article
import time
#import hashlib
import pymongo
from pymongo import MongoClient
try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['crawledurls'] #連結到該database的table
    #collection2 = db['crawledurlsTest2']
    print("Connects to MongoDB successfully!!")
except:
    print('Cannot connect to MongoDB server!!')

#----------------------------------------------------------------------------------------------------

"""def getUnixtime():
    unixtime = int(time.time())  #標記時間戳(系統時間)
    return unixtime

def getMd5(url):
    hash_object = hashlib.md5(url.encode())
    MD5code = hash_object.hexdigest()  #將url轉成MD5並且存取下來
    return MD5code

def getContent(url):
    art = Article(url, language = "zh")
    try:
        art.download() #載入文章
        art.parse()
    except:
        print('cannot download texts!!')
        pass
    art_text = art.text.replace('\n', '').replace('\'', '').replace('\"', '').replace("\xa0", "").replace("\u3000", "").replace("\xa06", "").replace("\xa03", "").replace("\xa02", "").replace("\xa01", "").strip()#word_cnt.most_common()[:10]                                                                                                                                                                                                                                                                
    return art_text

def jiebaAnalysis(content):
    jieba.set_dictionary('c:\\users\\defaultuser0\\dict.txt') #結巴斷詞字庫
    words = jieba.cut(content, cut_all=False)
    words = jieba.analyse.set_stop_words('C:\\Users\\defaultuser0\\stopwords.txt') #中文停用詞字庫
    words = jieba.analyse.extract_tags(str(content),15) #利用jieba.analyse來計算文本TF-IDF關鍵詞
    return words"""
#
#----------------------------------------------------------------------------------------------------

#利用無窮迴圈來檢查資料庫
#db.collection.find().limit(1).sort({$natural:-1})
#collection.find_one({},{'_id':0}).limit(1).sort({"$natural":-1})["url"]
while True:
    try:
        url = collection.find_one()["url"] #find_one({},{'_id':0})["url"]
        unixtime = getUnixtime()
        md5 = getMd5(url)
        artContent= getContent(url)
        tfidf = jiebaAnalysis(artContent)
        if len(url) > 15:
        #try:                       #try to set _id to MD5 code
            collection2.insert_one({"_id":md5}) #insert MD5code into MongoDB
            collection2.update_one({"_id":md5},{"$set":{"unix_time":unixtime}}) #insert unixtime into MongoDB
            if len(artContent) > 100:
                collection2.update_one({"_id":md5},{"$set":{"content":artContent}}) #insert content into MongoDB
            else:
                print("This article is too short.")
                pass
            collection2.update_one({"_id":md5},{"$set":{"url":url}})
            collection2.update_one({"_id":md5},{"$set":{"TD-IDF":str(tfidf).replace("[", "").replace("]", "").replace("'", "")}})
            collection.delete_one({"unix_time":{"$exists":False}}) #delete_one({"unix_time":{"$exists":False}})
            print("Analysis done! Check your database.")
        #except:
            #print("Some error occurs!!")
            #pass
        else:
            print("Url not found.")
    except:
        print("No urls found in the cache!!")
        time.sleep(10)

#------------------------------------------------------------------------------------------------
