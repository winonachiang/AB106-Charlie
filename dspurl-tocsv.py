#把爬好的url整理成CSV檔
import csv
import time
from pymongo import MongoClient
from collections import Counter
try:
    client = MongoClient('127.0.0.1', 27017) 
    db = client['admin'] #連結到mongoDB裡的database
    collection = db['interestgroups']
except:
    print('Cannot connect to MongoDB server!!')

print("start writing to csv file")

start = time.time()
#創一個CSV檔
csvfile  = open('/home/c29559810/s3/dsp_csv/dspurl.csv', 'w', newline='', encoding='utf8')
#將輸入CSV檔的規則訂好
spamwriter = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#讀取資料庫
documents = collection.find()

limit = 100000
file_count = 0
doc_list = []
for d in documents:
    doc_list.append(d)
    if len(doc_list) < limit:
        continue
    file_name = str(file_count) + ".csv"
    with open(file_name, 'w', newline='', encoding='utf8') as file:
        for doc in doc_list[:-1]:
            spamwriter = csv.writer(file, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([doc['_id'], doc['url'], doc['keywords'].replace("'",'').replace(",","")])
#
end = time.time()
elapsed = end - start
print('finished writing to csv file')
print ("Time taken: ", elapsed, "seconds.")
