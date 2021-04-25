import os
import time
import json
import math
import tools
import requests
import pymongo
import datetime
import pandas as pd


# https://eniu.com/chart/pea/sh601318/t/all
PATTERN = 'https://eniu.com/chart/pea/{}/t/all'


def getPE(symbol):
    data = {}
    url = PATTERN.format(symbol.lower())
    print(url)
    response = requests.get(url).json()
    date = response['date']
    pe = response['pe_ttm']
    for i in range(len(pe)):
        key = symbol + date[i]
        data[key] = pe[i]
    tools.saveJson(data, './snowball/pe.json')
    return data


def fetch(save=False):
    data = []
    url = PATTERN.format('sh601318')
    response = requests.get(url).json()
    print(len(response['date']))
    print(len(response['pe_ttm']))
    # print('Pages to fetch:', page)
    # for i in range(page):
    #     url = PATTERN.format(i + 1)
    #     response = requests.get(url, headers=headers).json()
    #     stocks = response['data']['list']
    #     data.extend(stocks)
    #     print('|', end='', flush=True)
    #     time.sleep(2)
    # print()
    # data = normalize(data)
    # if(save == True):
    #     tools.saveCSV(data, './snowball/pe.json')
    # return data


def normalize(data):
    for i in data:
        if(i.__contains__('has_follow')):
            del i['has_follow']
        if(i.__contains__('followers')):
            del i['followers']
    return data


if __name__ == '__main__':
    # fetch(True)
    getPE('SH601318')
