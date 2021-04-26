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


def update():
    cnt = 0
    files = os.listdir('./snowball/pe')
    files = ['SZ000001.json', 'SZ000002.json']

    for f in files:
        aStock = tools.loadJson('./snowball/pe/' + f, log=False)
        for date, pe in aStock.items():
            target = quoteDao.find_one({'symbol': f.split('.')[0], 'date': date})
            if(target is not None):
                quoteDao.update_one({'_id': target['_id']}, {'$set': {'pe_ttm': pe}})
        cnt = cnt + 1
        print('\rProgerss:', cnt, format(cnt * 100 / len(files), '.2f') + '%', end='')


if __name__ == '__main__':
    # merge()
    # getPE('SH601318')
    update()
