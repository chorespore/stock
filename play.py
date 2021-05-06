import dao
import find
from pypinyin import lazy_pinyin


def go():
    res = find.getTradingDay('2021-02-01', 5)
    print(res)


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
