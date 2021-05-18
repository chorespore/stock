import dao
import find
import fetch
import tools
import datetime
import numpy as np
from pypinyin import lazy_pinyin


def go():
    today = fetch.hasSaved()
    print(today)


def genKeyword(symbol, name):
    arr = lazy_pinyin(name)
    full = ''
    abbr = ''
    for i in arr:
        abbr = abbr + i[0].lower()
        full = full + i.lower()
    return symbol.lower() + '-' + abbr + '-' + full


if __name__ == '__main__':
    # go()
    # dao.deleteField()
    data = tools.loadCSV('./snowball/stock_prices.csv')
    res = np.array(data.iloc[2000:2010, 1])
    print(res)
