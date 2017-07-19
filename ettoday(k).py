from newspaper import Article
from urllib.request import urlopen
#import jieba
from collections import Counter

def getArticle(url):
	art_dict = {}
	art = Article(url, language = "zh")
	art.download()
	art.parse() 
	#That is one definite death I can pre
	art_text = art.text.replace("\n", " ")   #word_cnt.most_common()[:10]
	#art_title = art.title
	art_source = art.source_url
	art_url = art.url.replace("\n", "")
	
	art_dict["content"] = art_text
	art_dict["url"] = art_url
	art_dict["source"] = art_source
	print(art_dict)

	return art_dict


f = open('C:\\Users\\CF_NB.CF.000\\uncrawledurls\\ettoday(k).txt','rt')
lines = f.readlines()#.decode("utf-8")
#print(lines).replace("\n", " ")

for i in lines:
	#urlopen(i)#.decode("utf-8")
	#print(i)
	getArticle(i)
