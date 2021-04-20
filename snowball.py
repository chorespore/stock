import os
import time
import json
import math
import requests
import pymongo
import datetime
import pandas as pd


PATTERN = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=90&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1618316808034'
headers = {
    'Cookie': 'acw_tc=2760820516183175992951366e837ab495f500514af90d4e45b8746feb9e28; s=c511ggov7i; xq_a_token=cc6a2aedef8a96868eb7257aef4a2ba6e222d2c6; xq_r_token=3e168659e8b7d1863aff7a493cfc3398f438abe3; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYxOTkyMzQ2NiwiY3RtIjoxNjE4MzE3NTQ5NjI4LCJjaWQiOiJkOWQwbjRBWnVwIn0.LUuPfuYXEfxY9KfeY_XbFla-Q2Z4QrksjRNaLJ_goIJIRRunvSDDcmtvFlRHNyYadMclFRm5sjnAvLID5GLTr574b20B30jp366GzY9lNX3UB1Pe4d38GY1IPnF1WFNbN2kiDeIVh_Rx1jPMF6BEklKAalLMAdf5POQEpVKi8qe60gZExZjPQZf5R1NRQPQn8BQcYvJEYMpUCeS33_wnt4nbjNFSwkCAO7b7UjK_lxMer1EWFoRDsIvCFRhXaknWsvSdtqhYFcFFAxegh5i1v0m9vCE-NqFGFe75Bri9j3qq9KG2mEvVlgpC19hm1wiaAKeSbAe5AUaElPPVRQFsUA',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}


def fetch(save=False):
    data = []
    page = getPageSize()
    print('Pages to fetch:', page)
    for i in range(page):
        url = PATTERN.format(i + 1)
        response = requests.get(url, headers=headers).json()
        stocks = response['data']['list']
        data.extend(stocks)
        print('|', end='', flush=True)
        time.sleep(2)
    print()
    data = normalize(data)
    if(save == True):
        saveJson(data)
    return data


def normalize(data):
    for i in data:
        if(i.__contains__('has_follow')):
            del i['has_follow']
        if(i.__contains__('followers')):
            del i['followers']
    return data


def getPageSize():
    url = PATTERN.format(1)
    total = requests.get(url, headers=headers).json()['data']['count']
    return math.ceil(total / 90)


def saveJson(data):
    filename = './snowball/{}.json'.format(str(datetime.datetime.now().date()))
    with open(filename, 'w') as file_obj:
        json.dump(data, file_obj)
        print(len(data), 'items saved')


def loadJson(filename):
    with open(filename) as file_obj:
        data = json.load(file_obj)
        print(len(data), 'items loaded form', os.path.basename(filename))
        return data


def saveCSV(data):
    df = pd.DataFrame.from_dict(data)
    df.to_csv('{}.csv'.format(str(datetime.datetime.now().date())))
    print(len(data), 'items saved to CSV')


if __name__ == '__main__':
    # fetch(True)
    d = loadJson('./snowball/2021-04-19.json')
    # print(len(d))
    # print(d)
    d = normalize(d)
    print(d)
