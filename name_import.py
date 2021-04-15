import time
import json
import requests
import pymongo
import datetime
import pandas as pd

PAGE = 49
data = []
headers = {
    'Cookie': 'acw_tc=2760820516183175992951366e837ab495f500514af90d4e45b8746feb9e28; s=c511ggov7i; xq_a_token=cc6a2aedef8a96868eb7257aef4a2ba6e222d2c6; xq_r_token=3e168659e8b7d1863aff7a493cfc3398f438abe3; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxOTkyMzQ2NiwiY3RtIjoxNjE4MzE3NTQ5NjI4LCJjaWQiOiJkOWQwbjRBWnVwIn0.LUuPfuYXEfxY9KfeY_XbFla-Q2Z4QrksjRNaLJ_goIJIRRunvSDDcmtvFlRHNyYadMclFRm5sjnAvLID5GLTr574b20B30jp366GzY9lNX3UB1Pe4d38GY1IPnF1WFNbN2kiDeIVh_Rx1jPMF6BEklKAalLMAdf5POQEpVKi8qe60gZExZjPQZf5R1NRQPQn8BQcYvJEYMpUCeS33_wnt4nbjNFSwkCAO7b7UjK_lxMer1EWFoRDsIvCFRhXaknWsvSdtqhYFcFFAxegh5i1v0m9vCE-NqFGFe75Bri9j3qq9KG2mEvVlgpC19hm1wiaAKeSbAe5AUaElPPVRQFsUA',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

client = pymongo.MongoClient(host='mongodb://localhost', username='chao', password='mongo2020')
db = client["stock"]
nameColl = db["name"]


def importData():
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
            nameColl.update_many({'symbol': s}, {"$set": {"symbol": parts[1]+parts[0]}})
    print(len(symbolSet))


def fetch(page):
    for i in range(page):
        pattern = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=90&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1618316808034'
        url = pattern.format(i+1)
        response = requests.get(url, headers=headers).json()
        stocks = response['data']['list']
        data.extend(stocks)
        print('|', end='', flush=True)
        time.sleep(2)
    print()
    saveJson(data)


def saveJson(data):
    filename = './snowball/{}.json'.format(str(datetime.datetime.now().date()))
    with open(filename, 'w') as file_obj:
        json.dump(data, file_obj)
        print(len(data), 'items saved')


def loadJson(filename):
    global data
    with open(filename) as file_obj:
        data = json.load(file_obj)
        print(len(data), 'items loaded')


def saveCSV(data):
    df = pd.DataFrame.from_dict(data)
    df.to_csv('{}.csv'.format(str(datetime.datetime.now().date())))
    print(len(data), 'items saved to CSV')


if __name__ == '__main__':
    fetch(PAGE)
    # saveJson(data)
    # loadJson('./docker-compose/data/2021-04-13.json')
    # importData()
    # updataSymbol()
