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
    contents = soup.select('#text > div')
    contents_dict = {}
    for page in range(len(contents)):
        contents_dict[page+1] = contents[page].text.replace('\n', '').replace('\'', '').replace('\"', '').strip()
    #article = contents.text.replace('\n', '').replace('\'', '').replace('\"', '').strip()
    articles_dict['contents'] = contents_dict #article
    articles_dict['url'] = url.replace("\n", "")
    articles_dict['source'] = 'https://disp.cc/'
    print(articles_dict)

    return articles_dict


f = open('C:\\Users\\CF_NB.CF.000\\uncrawledurls\\disp(old).txt','rt')
lines = f.readlines()#.decode("utf-8")
#print(lines).replace("\n", " ")
for i in lines:
    urlopen(i)#.decode("utf-8")
    crawlPage(i)

	#print(i)

#crawlPage('https://disp.cc/b/733-74wY')