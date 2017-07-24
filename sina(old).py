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
    contents = soup.select('#artiBlock > p')
    contents_dict = {}
    for page in range(len(contents)):
        contents_dict[page+1] = contents[page].text.replace('\n', '').replace('\'', '').replace('\"', '').replace("\xa0","").replace("\u200b", "").replace("\xa0", "").replace("\xa06", "").replace("\u3000", "").strip()
    #article = contents.text.replace('\n', '').replace('\'', '').replace('\"', '').strip()
    articles_dict['contents'] = contents_dict #article
    articles_dict['url'] = url.replace("\n", "")
    articles_dict['source'] = 'http://m.ipop.sina.com.tw/'
    print(articles_dict)

    return articles_dict
#public static void main([args] Strings){
#   system.out.println("Hello World!")
#}

f = open('C:\\Users\\CF_NB.CF.000\\uncrawledurls\\sina(old).txt','rt')
lines = f.readlines()#.decode("utf-8")
#print(lines).replace("\n", " ")
for i in lines:
    #urlopen(i) #Do not use this function when crawling.
    crawlPage(i)

	#print(i)

#crawlPage('https://www.ct.org.tw/1244979')
