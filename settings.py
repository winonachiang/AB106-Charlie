# -*- coding: utf-8 -*-

"""
    eve-demo settings
    ~~~~~~~~~~~~~~~~~
    Settings file for our little demo.
    PLEASE NOTE: We don't need to create the two collections in MongoDB.
    Actually, we don't even need to create the database: GET requests on an
    empty/non-existant DB will be served correctly ('200' OK with an empty
    collection); DELETE/PATCH will receive appropriate responses ('404' Not
    Found), and POST requests will create database and collections when needed.
    Keep in mind however that such an auto-managed database will most likely
    perform poorly since it lacks any sort of optimized index.
    :copyright: (c) 2016 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os
import hashlib
# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_HOST = os.environ.get('MONGO_HOST', '10.8.16.215')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)

MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'admin')
#

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']


#
# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

def encodeUrl(url):
    hash_object = hashlib.md5(url.encode())
    MD5code = hash_object.hexdigest()
    url = {}
    url['url'] = url
    url['_id'] = MD5code
    print(url)
    return url
#
tasks = {
	'id' : encodeUrl("http://eznewlife.com/150535/以前都考100分？兒子竟意外翻出「爸爸的國中考卷」猛一看…網友都要跪惹！"), 
    'title' :  "newurl" ,
    'description' :  "this is to decide where this url should be sent to" ,
    'done' :  False
}

DOMAIN = {
	"url" : tasks,
}




#urlcompiled = encodeUrl("http://eznewlife.com/150535/以前都考100分？兒子竟意外翻出「爸爸的國中考卷」猛一看…網友都要跪惹！")

#DOMAIN = {
#    'urlcompiled': urlcompiled,
#}
