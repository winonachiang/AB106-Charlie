import requests
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import pickle
import json
import time
import datetime
import hashlib
datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def crawlPage(url):

    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')
    articles_dict = {} 
    contents = soup.select('div.row.article_content.main_article > div > div > p') #like GPS huh~~

    #contents_dict = {}
    #for page in range(len(contents)):
        #contents_dict[page+1] = contents[page].text.replace('\n', '').replace('\'', '').replace('\"', '').replace("\xa0", "").replace("\u3000", "").replace("\xa06", "").replace("\xa03", "").replace("\xa02", "").replace("\xa01", "").strip()
    content = contents
    unix_time = int(time.time())
    hash_object = hashlib.md5(url.encode())
    MD5code = hash_object.hexdigest()
    
    
    articles_dict['content'] = content
    articles_dict['url'] = url.replace("\n", "")
    articles_dict["unix_time"] = unix_time
    articles_dict["datetime"] = datetime  
    articles_dict["MD5"] = MD5code
    print(articles_dict)

    return articles_dict

f = open('C:\\Users\\CF_NB.CF.000\\uncrawledurls(not crawled)\\beautimode.txt','r')
lines = f.readlines()#.decode("utf-8")
#print(lines).replace("\n", " ")
for i in lines:
    urlopen(i)#.decode("utf-8")
    crawlPage(i)
#rawlPage('https://disp.cc/b/163-9kTh')