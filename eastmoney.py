import os
import time
import math
import json
import requests
import pymongo
import datetime
import pandas as pd

data = []

fieldMap = {'f2': 'current', 'f3': 'percent', 'f4': 'change', 'f12': 'symbol', 'f14': 'name',
            'f15': 'high', 'f16': 'low', 'f17': 'open', 'f18': 'close', 'f23': 'pe', 'f115': 'pb_ttm'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

PATTERN = 'http://58.push2.eastmoney.com/api/qt/clist/get?pn={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1618489972043'


def createFolder(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def saveJson(data):
    createFolder('./snowball')
    filename = './snowball/em{}.json'.format(str(datetime.datetime.now().date()))
    with open(filename, 'w') as file_obj:
        json.dump(data, file_obj)
        print(len(data), 'items saved')


def fetch():
    page = getPageSize()
    print('Pages to fetch:', page)
    for i in range(1, page):
        url = PATTERN.format(i)
        raw = requests.get(url, headers=headers).json()['data']
        total = raw['total']
        stockList = raw['diff']
        data.extend(stockList)
        print('|', end='', flush=True)
        time.sleep(2)
    print()
    saveJson(data)


def getPageSize():
    url = PATTERN.format(1)
    total = requests.get(url, headers=headers).json()['data']['total']
    return math.ceil(total/20)+1


fetch()
