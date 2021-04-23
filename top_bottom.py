import dao
import find
import pandas as pd


quoteDao = dao.quotes
nameDao = dao.names


def topBottom():
    results = []
    cnt = 0
    total = nameDao.count_documents({})
    print('Items to search:', total)
    for name in nameDao.find():
        res = quoteDao.find({'symbol': name['symbol'], "$or": [{"change_rate": {"$gt": 9.9}}, {"change_rate": {"$lt": -9.9}}]}).sort('date', 1)
        aStock = []
        for i in res:
            del i['_id']
            aStock.append(i)

        for i in range(len(aStock) - 1):
            quote = aStock[i]
            # print((quote['high'] - quote['pre_close']) / quote['pre_close'], (quote['pre_close'] - quote['low']) / quote['pre_close'])
            if((quote['high'] - quote['pre_close']) / quote['pre_close'] > 0.099 and (quote['pre_close'] - quote['low']) / quote['pre_close'] > 0.099):
                item = {'name': name['name'], 'symbol': name['symbol'], 'date': quote['date']}
                item['d1'] = quote['change_rate']
                d2 = quoteDao.find_one({'symbol': name['symbol'], 'date': find.nextTradingDay(quote['date'])})
                if(d2 is not None):
                    item['d2'] = d2['change_rate']
                else:
                    item['d2'] = 0.0
                results.append(item)
        cnt = cnt + 1
        print('\rProgerss:', str(len(results)), format(cnt * 100 / total, '.2f') + '%', end='')
    print()
    saveCSV(results)


def saveCSV(data):
    df = pd.DataFrame.from_dict(data)
    df.to_csv('./snowball/TopBottom.csv', encoding="utf_8_sig")
    print(len(data), 'items saved to CSV')


if __name__ == '__main__':
    topBottom()
