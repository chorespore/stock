import dao
import find
import fetch
import csv
import tools
import datetime
import numpy as np
import pandas as pd
from pypinyin import lazy_pinyin


def go():
    tmp_lst = []
    with open('./snowball/000001.SZ.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    stock_quotes = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
    for i, row in stock_quotes.iterrows():
        row['open'] = (float(row['open']) - float(row['pre_close'])) / float(row['pre_close']) * 100 + 10.1
        row['high'] = (float(row['high']) - float(row['pre_close'])) / float(row['pre_close']) * 100 + 10.1
        row['low'] = (float(row['low']) - float(row['pre_close'])) / float(row['pre_close']) * 100 + 10.1
        row['close'] = (float(row['close']) - float(row['pre_close'])) / float(row['pre_close']) * 100 + 10.1
    stock_quotes.to_csv('./snowball/SZ000001.csv', index=False)


def genKeyword(symbol, name):
    arr = lazy_pinyin(name)
    full = ''
    abbr = ''
    for i in arr:
        abbr = abbr + i[0].lower()
        full = full + i.lower()
    return symbol.lower() + '-' + abbr + '-' + full


if __name__ == '__main__':
    go()
    # dao.deleteField()
    # data = tools.loadCSV('./snowball/stock_prices.csv')
    # res = np.array(data.iloc[2000:2010, 1])
    # print(res)
