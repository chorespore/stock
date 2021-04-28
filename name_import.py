import time
import json
import requests
import pymongo
import datetime
import snowball
import pandas as pd
from pypinyin import lazy_pinyin


client = pymongo.MongoClient(host='mongodb://localhost', username='chao', password='mongo2020')
db = client["stock"]
nameColl = db["name"]


def importData(data):
    doc = []
    nameColl.drop()
    stockSet = set()
    for i in data:
        if(i['symbol'] in stockSet):
            continue
        stockSet.add(i['symbol'])
        item = {}
        item['symbol'] = i['symbol']
        item['name'] = i['name']
        item['keyword'] = genKeyword(i['symbol'], i['name'])
        doc.append(item)
    nameColl.insert_many(doc)
    print(nameColl.count_documents({}), 'items saved to mongo')

    createIndex()


def genKeyword(symbol, name):
    full = ''
    abbr = ''
    arr = lazy_pinyin(name)
    for i in arr:
        abbr = abbr + i[0].lower()
        full = full + i.lower()
    return symbol.lower() + '-' + abbr + '-' + full


def updataSymbol():
    symbolSet = set()
    res = nameColl.find()
    for i in res:
        s = i['symbol']
        if(s not in symbolSet):
            symbolSet.add(s)
            parts = s.split('.')
            print(s, parts[1] + parts[0])
            nameColl.update_many(
                {'symbol': s}, {"$set": {"symbol": parts[1] + parts[0]}})
    print(len(symbolSet))


def createIndex():
    indexes = ['symbol', 'keyword']
    for idx in indexes:
        print('Creating index of', idx)
        nameColl.create_index([(idx, 1)], unique=True)


if __name__ == '__main__':
    # data = snowball.fetch()
    data = snowball.loadJson('./snowball/2021-04-19.json')
    importData(data)
