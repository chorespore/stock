import time
import json
import requests
import pymongo
import datetime
import snowball
import pandas as pd


client = pymongo.MongoClient(host='mongodb://localhost', username='chao', password='mongo2020')
db = client["stock"]
nameColl = db["name"]


def importData(data):
    doc = []
    nameColl.drop()
    for i in data:
        item = {}
        item['symbol'] = i['symbol']
        item['name'] = i['name']
        doc.append(item)
    nameColl.insert_many(doc)
    print(nameColl.count_documents({}), 'items saved to mongo')

    indexes = ['symbol']
    for idx in indexes:
        print('Creating index of', idx)
        nameColl.create_index([(idx, 1)])


def updataSymbol():
    symbolSet = set()
    res = nameColl.find()
    for i in res:
        s = i['symbol']
        if(s not in symbolSet):
            symbolSet.add(s)
            parts = s.split('.')
            print(s, parts[1]+parts[0])
            nameColl.update_many(
                {'symbol': s}, {"$set": {"symbol": parts[1]+parts[0]}})
    print(len(symbolSet))


if __name__ == '__main__':
    data = snowball.fetch()
    # data=snowball.loadJson('')
    importData(data)
