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

def get9618(url):

    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')

    articles_dict = {}
    contents = soup.select('#mainarea > div.diary-body > p')
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
    articles_dict['contents'] = contents_dict 
    #print(articles_dict)

    return articles_dict


#f = open('C:\\Users\\CF_NB.CF.000\\uncrawledurls(old)\\9618(old).txt','rt')
#lines = f.readlines()#.decode("utf-8")
#print(lines).replace("\n", " ")
#for i in lines:
    #urlopen(i)#.decode("utf-8")
    #get9618(i)

get9618('https://asia9618.nidbox.com/diary/read/8946172')
