import dao
import find
import pandas as pd

quoteDao = dao.quotes
nameDao = dao.names


def findShakes():
    results = []
    stop = 0
    for name in nameDao.find():
        # print(name)
        res = quoteDao.find({'symbol': name['symbol'], "$or": [{"change_rate": {"$gt": 9.9}}, {"change_rate": {"$lt": -9.9}}]}).sort('date', 1)
        aStock = []
        for i in res:
            del i['_id']
            aStock.append(i)

        stop = stop + 1
        if(stop == 10):
            saveCSV(results)
            return

        # print(aStock)

        window = []
        for i in range(1, len(aStock) - 1):
            if(find.nextTradingDay(aStock[i - 1]['date']) == aStock[i]['date']):
                if(len(window) == 2 and aStock[i]['change_rate'] < 0):
                    item = {'name': name['name'], 'symbol': name['symbol'], 'date': aStock[i - 2]['date']}
                    # item['d1'] = aStock[i - 2]['change_rate']
                    # item['d2'] = aStock[i - 1]['change_rate']
                    # item['d3'] = aStock[i]['change_rate']
                    item['d1'] = window[0]['change_rate']
                    item['d2'] = window[1]['change_rate']
                    item['d3'] = aStock[i]['change_rate']
                    item['d4'] = quoteDao.find_one({'symbol': name['symbol'], 'date': find.nextTradingDay(aStock[i]['date'])})['change_rate']
                    window.clear()
                    results.append(item)
                    print(item)
                    # print('\rPattern Found:', len(results), end='')
                elif(len(window) < 2 and aStock[i]['change_rate'] > 0):
                    # print(aStock[i]['change_rate'], aStock[i]['change_rate'] > 0)
                    window.append(aStock[i])
                else:
                    window.clear()
                    # print(quote['symbol'], quote['date'], quote['change_rate'])
    saveCSV(results)


def saveCSV(data):
    df = pd.DataFrame.from_dict(data)
    df.to_csv('./snowball/shake.csv', encoding="utf_8_sig")
    print(len(data), 'items saved to CSV')


if __name__ == '__main__':
    findShakes()
