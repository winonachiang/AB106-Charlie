#取得與mongoDB的連線
import jieba
import jieba.analyse
from newspaper import Article
import time
#import hashlib
import newspaper
import re
re_words = re.compile("[\u4e00-\u9fa5]+")
#import pymongo
#from pymongo import MongoClient
"""try:
    client = MongoClient('127.0.0.1', 27017)
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['crawledurls3'] #連結到該database的table
    print("Connects to MongoDB successfully!!")
except:
    print('Cannot connect to MongoDB server!')"""

#---------------------------------------------我是分隔線----------------------------------------------

#Get contents of articles and insert them into mongoDB
#Main program:
def getArticle(url):
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
    #unixtime = int(time.time())  #標記時間戳(系統時間)
    #hash_object = hashlib.md5(art_url.encode())
    #MD5code = hash_object.hexdigest()  #將url轉成MD5並且存取下來
    #match = re.findall(re_words, art_text)
    jieba.set_dictionary('C:\\Users\\defaultuser0\dict.txt')  #結巴斷詞字庫
    words = jieba.cut(art_text, cut_all=False)
    words = jieba.analyse.set_stop_words('C:\\Users\\defaultuser0\\stopwords.txt')
    words = jieba.analyse.extract_tags(str(art_text),15)  #利用jieba.analyse來計算文本TF-IDF關鍵詞
    art_dict["content"] = art_text         #switch to match
    art_dict["url"] = art_url
    #art_dict["source"] = "technews"
    #art_dict["unix_time"] = unixtime
    #art_dict["MD5"] = MD5code
    art_dict["TF-IDF words list"] = str(words).replace("[", "").replace("]", "")
    #art_dict["EnglishKwds"] = str(set(re.findall('[a-zA-Z]+', art_text))).replace("{", "").replace("}", "")
    print(art_dict)
    return art_dict
#
getArticle("http://www.chinatimes.com/newspapers/20170928000125-260204")
#-----------------------------------------------------------------------------------------------------

"""f = open('C:\\Users\\defaultuser0\\uncrawledurls(k)\\technews(k).txt','rt',encoding="utf8")
line = f.readlines()
for i in line:
    try:
        art_dict = getArticle(i)
        if len(art_dict['content']) < 65:
            print("Article is too short.")
            pass
        else:
            db.crawledurls3.insert_one(art_dict)
    except:
        print("There's no articles!!")
        pass"""

#-----------------------------------------------------------------------------------------------------
