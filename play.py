import dao
from pypinyin import lazy_pinyin


def go():
    arr = lazy_pinyin('N聪明')
    res = ''
    abbr = ''
    for i in arr:
        abbr = abbr + i[0].lower()
        res = res + i.lower()

    print(genKeyword('N聪明', 'SH002'))


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
