import os
import time
import json
import dao
import math
import tools
import requests
import datetime
import pandas as pd

quoteDao = dao.quotes

# pe_ttm: Price-to-Earning Ratio Trailing Twelve Months
PATTERN = 'https://eniu.com/chart/pea/{}/t/all'

err = []


def getPE(symbol):
    data = {}
    url = PATTERN.format(symbol.lower())
    response = requests.get(url).json()
    date = response['date']
    pe = response['pe_ttm']
    for i in range(len(pe)):
        data[date[i]] = pe[i]
    tools.saveJson(data, './snowball/pe/{}.json'.format(f), log=False)
    time.sleep(2)
    return data


def getSymbols():
    res = []
    files = os.listdir('./allstock')
    for i in files:
        parts = i.split('.')
        res.append(parts[1] + parts[0])
    return res


def merge():
    data = []
    files = os.listdir('./snowball/pe')
    for f in files:
        item = {}
        aStock = tools.loadJson('./snowball/pe/' + f, log=False)
        item['symbol'] = f
        item['data'] = aStock
        data.append(item)
    tools.saveJson(data, './snowball/allPE.json')
    # print(files)


def update():
    cnt = 0
    files = os.listdir('./snowball/pe')
    files = ['SZ000001.json', 'SZ000002.json']
    for f in files:
        aStock = tools.loadJson('./snowball/pe/' + f, log=False)
        for date, pe in aStock.items():
            target = quoteDao.find_one({'symbol': f.split('.')[0], 'date': date})
            if(target is not None):
                quoteDao.update_one({'_id': target['_id']}, {'$set': {'pe_ttm': pe}})
        cnt = cnt + 1
        print('\rProgerss:', cnt, format(cnt * 100 / len(files), '.2f') + '%', end='')


def fetch(save=False):
    cnt = 0
    symbols = getSymbols()
    files = set(os.listdir('./snowball/pe'))
    for i in symbols:
        if(i + '.json' not in files):
            try:
                getPE(i)
            except BaseException:
                err.append(i)
                print('\texcption', i)
        cnt = cnt + 1
        print('\rProgerss:', cnt, i, format(cnt * 100 / len(symbols), '.2f') + '%', end='')


def normalize(data):
    for i in data:
        if(i.__contains__('has_follow')):
            del i['has_follow']
        if(i.__contains__('followers')):
            del i['followers']
    return data


if __name__ == '__main__':
    fetch()
    print(err)
