import jieba
import jieba.analyse
import requests
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import time
import datetime
import pickle
datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getGameettoday(url):

    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')

    articles_dict = {}
    contents = soup.select('div.story > p')
    contents_dict = {}
    for page in range(len(contents)):
        contents_dict[page+1] = contents[page].text.replace('\n', '').replace('\'', '').replace('\"', '').replace("\xa0", "").replace("\u3000", "").replace("\xa06", "").replace("\xa03", "").replace("\xa02", "").replace("\xa01", "").strip()   
    unixtime = int(time.time())  #標記時間戳(系統時間)   
    hash_object = hashlib.md5(url.encode())
    MD5code = hash_object.hexdigest()  #將url轉成MD5並且存取下來
    jieba.set_dictionary('./dict.txt.big.txt')  #結巴斷詞字庫
    words = jieba.cut(contents_dict, cut_all=False) 
    words = jieba.analyse.set_stop_words('./stopwords.txt')  
    words = jieba.analyse.extract_tags(str(contents_dict),10)  #利用jieba.analyse來計算文本TF-IDF關鍵詞
    
    articles_dict['url'] = url.replace("\n", "")
    articles_dict['MD5'] = MD5code
    articles_dict['unix_time'] = unixtime
    articles_dict['datetime'] = datetime
    articles_dict["TF-IDF words list"] = str(words).replace("[", "").replace("]", "")
    articles_dict['contents'] = str(contents_dict).replace("{", "").replace("}", "").replace("1: ", "").replace("2: ", "").replace("3: ", "").replace("4: ", "").replace("5: ", "").replace("6: ", "").replace("7: ", "").replace("8: ", "").replace("9: ", "").replace("10: ", "").replace("11: ", "").replace("12: ", "").replace("13: ", "").replace("14: ", "").replace("15: ", "").replace("16: ", "").replace("17: ", "").replace("18: ", "").replace("19: ", "").replace("20: ", "").replace("21: ", "").replace("22: ", "").replace("23: ", "").replace("24: ", "").replace("25: ", "").replace("26: ", "").replace("'',", " ").replace("1'", "").replace("1 ", "").replace("\\t", "").replace("\\r", "")
    #print(articles_dict)

    return articles_dict


#f = open('C:\\Users\\CF_NB.CF.000\\uncrawledurls(old)\\gameettoday(old).txt','rt')
#lines = f.readlines()#.decode("utf-8")
#print(lines).replace("\n", " ")
#for i in lines:
    #urlopen(i)#.decode("utf-8")
    #getCnews(i)

getGameettoday('http://game.ettoday.net/article/892843.htm')
