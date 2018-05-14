import boto3
from botocore.client import Config
import os
from datetime import date, timedelta

# os.system("sudo rm *_0") #先移除前一天下載的檔案

yesterday = date.today() - timedelta(1) #昨天的日期
formatted_yes = yesterday.strftime('%Y-%m-%d') #讓s3 cli去下載昨天的
ACCESS_KEY_ID = 'AKIAJL65SMNW76NPFMJQ'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'cap-transaction' #指定到你的Bucket

# 連接到 S3
s3 = boto3.resource( #指定你的key_ID跟secret_key
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

s3 = boto3.resource('s3')
mybucket = s3.Bucket(BUCKET_NAME)
# if blank prefix is given, return everything)
bucket_prefix="domain-daily/%s" % formatted_yes
objs = mybucket.objects.filter(
    Prefix = bucket_prefix)

# download the files under the folder recursively
for obj in objs:
    path, filename = os.path.split(obj.key)
    s3.Object(BUCKET_NAME, obj.key).download_file('/home/c29559810/s3/impression_urls/'+ filename)
                                                #'D:\\s3\\impression_urls\\'+ filename