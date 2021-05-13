import dao
import find
import fetch
import datetime
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
    go()
