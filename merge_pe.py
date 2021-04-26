import os
import dao
import tools

quoteDao = dao.quotes


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


def peCoverage():
    total = 10358691
    pe = 0
    res = quoteDao.find({}, {'symbol': 1, 'pe_ttm': 1})
    for i in res:
        if(i.__contains__('pe_ttm')):
            pe = pe + 1
    print(pe, pe / total)


if __name__ == '__main__':
    # merge()
    # getPE('SH601318')
    peCoverage()
