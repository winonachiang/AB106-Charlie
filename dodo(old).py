import requests
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import pickle
import json
import datetime

def crawlPage(url):

    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')

    articles_dict = {}
    try: #例外處理，把HTTP404或是403、400的跳過
        contents = soup.select('#node-content')
    except:
        pass
    contents_dict = {}
    for page in range(len(contents)):
        contents_dict[page+1] = contents[page].text.replace('\n', '').replace('\'', '').replace('\"', '').replace('\t', '').replace('\u3000', '').replace('\r', '').replace('\xa0', '').strip()
    #article = contents.text.replace('\n', '').replace('\'', '').replace('\"', '').strip()
    articles_dict['contents'] = contents_dict #article
    articles_dict['url'] = url.replace("\n", "")
    articles_dict['source'] = 'http://www.dodo.orgs.one/'
    print(articles_dict)

    return articles_dict


f = open('C:\\Users\\CF_NB.CF.000\\uncrawledurls\\dodo.txt','rt')
lines = f.readlines()#.decode("utf-8")
#print(lines).replace("\n", " ")
for i in lines:
    #urlopen(i) #Do not use this function when crawling.
    crawlPage(i)

	#print(i)

#crawlPage('https://www.ct.org.tw/1244979')