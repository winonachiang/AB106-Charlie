import re
import pymongo
from pymongo import MongoClient
from collections import Counter
import multiprocessing
import os
from textblob import TextBlob
from textblob import Word
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))

#any idea for her present?
# 定義 stopwords
def defineStopWords():
    with open('C:\\Users\\defaultuser0\\stop-word-list.txt', 'r', encoding='utf8') as mysw:
        swlist = stopwords.words() + mysw.read().split(',')
        mysw.close()
    return swlist


#1 回傳處理過的字(某段落內所有字)
def get_parawds(content, swlist):
    words = str(TextBlob(content).words.lower())
    match = re.findall('[a-z]+', words)
    myFilter = re.compile(r'(\w)\1{2,}')
    filtered = [word for word in match if not myFilter.search(word)]
    parawds= []
    for word in filtered:
        if word not in swlist and len(word) > 2:
            finalWord = Word(word).singularize().lemmatize("v") #把單字單數化、原型化
            parawds.append(finalWord)
    return parawds


#2 傳入全文單詞清單(重複)，回傳詞頻字典
def wordcount(all_wds):
    wc_dict = Counter()
    for word in all_wds:
        if word not in wc_dict:
            wc_dict[word] = 1
        else:
            wc_dict[word] += 1
    return wc_dict


#3 找某個字在哪個不重複段落出現
def get_src(word, all_parawds):
    src = set([])
    for parawds in all_parawds:
        if word in parawds:
            src.add(str(all_parawds.index(parawds)+1))
    return list(src)

#4 傳入單詞、詞頻字典(wc_dict)、parawds集合(all_parawds)，補上單詞出現段落及TF值
def get_wdinfo(word, wc_dict, all_parawds, n):
    wdinfo = {}
    wdinfo['count'] = wc_dict[word]
    wdinfo['TF'] = wc_dict[word]/n
    wdinfo['from'] = get_src(word, all_parawds)
    return wdinfo

#5 更新資料庫 word_dict
def update_DB_word_dict(wds_info, DB_word_dict):
    for word in wds_info:
        DB_word_dict.update_one({'_id': word}, {'$inc': {'count':1}}, upsert=True)


#6 更新資料庫 news
def update_DB_news(art_id, wds_info, DB_news):
    for word in wds_info:
        tf = wds_info[word]['TF']
        src = wds_info[word]['from']
        DB_news.update_one({'_id': art_id}, {'$set':{'counted':'true'}}, upsert=True)
        DB_news.update_many({'_id': art_id}, {'$set':{'wordset':wds_info}}, upsert=True)


#7 [MAIN PROGRAM]
def wc(swlist, connection):
    #info('Child Process for wc()')

    connection = pymongo.MongoClient('127.0.0.1', 27017, maxPoolSize=10)
    db = connection.news
    DB_news = db['finalproject']
    DB_word_dict = db['word_dict_en']

    article = DB_news.find_one_and_update({'source':'NYT','counted': {'$exists': False}},{'$set':{'counted':'Processing...'}})
    content = article['content']                    #Change Sources
    art_id = article['_id']

    all_parawds = []
    for para_id in range(len(content)):
        try:    #set the value of empty paragraphs to null so that there won't be any missing paragraphs.
            parawds = get_parawds(content[str(para_id + 1)], swlist)
        except KeyError:
            parawds = []
        all_parawds.append(parawds)

    all_wds = [word for parawds in all_parawds for word in parawds]
    n = len(all_wds)
    wds_set = set(all_wds)
    wc_dict = wordcount(all_wds)

    wds_info = {}
    for word in wds_set:
        wds_info[word] = get_wdinfo(word, wc_dict, all_parawds, n)

    update_DB_news(art_id, wds_info, DB_news)
    update_DB_word_dict(wds_info, DB_word_dict)

    connection.close()

    print('_id: %s \twordcount finished!\t%s words counted.' % (art_id,n))

    # message = '_id: %s \twordcount finished!\t%s words counted.' % (art_id,n)
    # return message

connection = pymongo.MongoClient('127.0.0.1', 27017)
db = connection.news
DB_news = db['finalproject']
DB_word_dict = db['word_dict_en']
swlist = defineStopWords()
#wc(swlist, connection)

#8
#def info(title):
    #print(title,', process id:', os.getpid())
    # print('module name:', __name__)
    # print('parent process:', os.getppid())
    # print('process id:', os.getpid())
#9
def run(swlist):
    swlist = defineStopWords()
    connection = pymongo.MongoClient('127.0.0.1', 27017, maxPoolSize=10)
    wc(swlist, connection)

objects = DB_news.find({"source":"NYT","counted":{"$exists":False}})
for obj in objects:
    try:
        run(swlist)
    except:
        DB_news.find_one_and_update({"source":"NYT","counted":"true","wordset":None},{'$set':{"counted":"failed"}})
        print("Odd strings in the contents.")
        pass
#
#------------------------------------------github version-------------------------------------------
