import dao
import find
from pypinyin import lazy_pinyin


def go():
    a=[1,4,6,2]
    a.sort()
    print(a)

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
