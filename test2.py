import jieba
import jieba.analyse
import requests
from collections import Counter
import re
import pickle
import operator
from operator import itemgetter
import math
import os
import pymongo
from pymongo import MongoClient
jieba.set_dictionary('C:\\Users\\defaultuser0\\dict.txt')
with open('C:\\Users\\defaultuser0\\stopwords.txt','r',encoding="utf8") as f:
    stopwords = f.read() #定義好stopwords，記得不要用readlines，最好都用read()
re_words = re.compile("[\u4e00-\u9fa5]+")

#-----------------------------------------------------------------------------------------------------

#1 回傳處理過的字(一篇文內所有字)
def get_parawds(content, swlist):
    words = [word for word in jieba.cut(content, cut_all=False) if word not in stopwords]
    #match = re.sub("[a-z,A-Z,V,I,A,0-9,.,......,「,」,......,《,》,Ｘ,▉,✈,一,╰,︶,╯,\,ω,∀,♥,Ｑ,╱,ω,╴,﹀,︵,〞,Ω,─,▁,◢,◣,●,►,◎,++,～,˙,█,…,Ⅲ,↑,＝,\,Ⅱ,×,∕,α,◤,◥,﹏,⊙,┼,┤,『,』,∵,∴,▏,ˋ,↓,│,◆,【,】,▽,★,☆,■,▲,φ,○,┴,├,▌,___,￣,ㄅ-ㄥ,▼,▔,→,═,┬,┘,┌,ㄧ,←,╭,╮,\,．,「,」,ㄨ,〒,▃,▄,▅,▇,／]", "", str(words))
    match = re.findall(re_words, str(words))
    parawds= []
    for word in match:
        if word not in swlist:
            finalWord = word #去除掉stopwords之後的字元
            parawds.append(finalWord)
    #print(parawds)
    return parawds

#
#2 傳入全文單詞清單(重複)，回傳詞頻字典
def wordcount(all_wds):
    wc_dict = Counter()
    for word in all_wds:
        if word not in wc_dict:
            wc_dict[word] = 1
        else:
            wc_dict[word] += 1
    return wc_dict

#4 傳入單詞、詞頻字典(wc_dict)、parawds集合(all_parawds)，補上單詞出現段落及TF值
def get_wdinfo(word, wc_dict, all_parawds, n):
    wdinfo = {}
    wdinfo['count'] = wc_dict[word]
    wdinfo['TF'] = wc_dict[word]/n
    return wdinfo

#5 更新資料庫 word_dict2
def update_DB_word_dict2(wds_info, DB_word_dict):
    for word in wds_info:
        DB_word_dict.update_one({'_id': word}, {'$inc': {'count':1}}, upsert=True)

#6 更新資料庫 crawledurls2
def update_DB_news(art_id, wds_info, DB_news):
    for word in wds_info:
        tf = wds_info[word]['TF']
        DB_news.update_one({'_id': art_id}, {'$set':{'counted':'true'}}, upsert=True)
        DB_news.update_many({'_id': art_id}, {'$set':{'wordset':wds_info}}, upsert=True)
                #update_many的目的是因為wordset不可能只有一個字

#-----------------------------------------------------------------------------------------------------

#code below is the main program that runs the whole functions
connection = pymongo.MongoClient('127.0.0.1', 27017, maxPoolSize=10)
db = connection.admin
DB_news = db['crawledurls3']
DB_word_dict = db['word_dict3']
def wc(swlist, connection):
    connection = pymongo.MongoClient('127.0.0.1', 27017, maxPoolSize=10)
    db = connection.admin
    DB_news = db['crawledurls3']
    DB_word_dict = db['word_dict3']
    articles = DB_news.find_one_and_update({'source':'epochtime','counted':{'$exists': False}},{'$set':{'counted':'Processing...'}})
                                            #Change Sources
    contents = articles['content']
    art_id = articles['_id']
    all_parawds = get_parawds(contents, stopwords)#回傳每篇文章處理過的字

    all_wds = all_parawds   #[word for parawds in all_parawds for word in parawds]
    n = len(all_wds) #計算一篇文章總辭數(有重複字)
    wds_set = set(all_wds) #每篇文章的詞庫，此步已經去掉重複詞
    wc_dict = wordcount(all_wds) #計算每篇文章每個詞出現的次數，也就是詞頻

    wds_info = {}
    for word in wds_set:
        wds_info[word] = get_wdinfo(word, wc_dict, all_parawds, n)
    update_DB_news(art_id, wds_info, DB_news)
    update_DB_word_dict2(wds_info, DB_word_dict)

    #connection.close()
    print('_id: %s \twordcount finished!\t%s words counted.' % (art_id,n))

def run(swlist):
    swlist = stopwords
    connection = pymongo.MongoClient('127.0.0.1', 27017, maxPoolSize=10)
    wc(swlist, connection)
                                                            #記得要改回False!!!!
"""objects = DB_news.find({"source":"epochtime","counted":{"$exists":False}})
for obj in objects:
    #run(stopwords)
    try:
        run(stopwords)
    except:
        DB_news.find_one_and_update({"source":"epochtime","counted":"true","wordset":None},{'$set':{"counted":"failed"}})
        print("Odd strings in the contents.")
        pass"""
#run(stopwords)

#---------------------------------------------------------------------------------------------------
#Life won't always be as smooth as you wish it'd be.
# 輸入兩個collections，計算總篇數 N，& 更新(計算出) word_dict2 中的 idf 值，主要目的是要計算每詞的IDF值
def updateIDF(N, DB_word_dict):
    word_dict = DB_word_dict.find()
    for word in word_dict:
        idf = math.log10(N/word['count']) #word['count']是該字出現過的篇數，記得要加1
        DB_word_dict.update_one({"_id": word['_id']}, {"$set":{"IDF":idf}})
    print("IDF in word_dict3 has been updated.")
#updateIDF(12552, DB_word_dict)

#最後一步: 計算Keywords
#input一篇文章，與 DB_word_dict 比對該文章wordset裡頭的字詞
#計算該文章 wordset 的 TF-IDF，排序取前10獲得keywords_dict

def findkeywords(wordset, DB_word_dict):
    tfidf_dict = {}
    for word in wordset['wordset']:
        ref = DB_word_dict.find_one({'_id':word}) #此處的word是wordset裏頭的每一個詞，對應到word_dict裏頭的詞
        try:
            tfidf = wordset['wordset'][word]['TF']*ref['IDF'] #比對兩個collections，計算TF-IDF值
            tfidf_dict[word] = tfidf
        except TypeError:
            #DB_art_keywords.find_one_and_update({'_id':wordset['_id']}, {'$unset':{word:1}})
            pass  #等下處理
    kw_TFIDF = sorted(tfidf_dict.items(), key=operator.itemgetter(1), reverse=True)[0:10]
    print(kw_TFIDF)
    return dict(kw_TFIDF)


#document = DB_news.find_one({"url":"https://disp.cc/b/163-8Gwo"})
#print(document['content'])
#print("------------------------------------------------以下是關鍵字-------------------------------------------------------")
#findkeywords(document, DB_word_dict)

#-----------------------------------------------------------------------------------------------

#words = DB_word_dict.find()
#for word in words:
    #print(word['_id']+" "+word['IDF'])
#Notice: string object doesn't have attribute "append".
#Try to make it a dictionary or a list.