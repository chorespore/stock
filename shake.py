import dao
import find
import pandas as pd

quoteDao = dao.quotes
nameDao = dao.names


def findShakes():
    results = []
    stop = 0
    cnt = 0
    total = nameDao.count_documents({})
    print('Items to search:', total)
    for name in nameDao.find():
        #  'date': {'$gt': '2016-06-01'},
        res = quoteDao.find({'symbol': name['symbol'], "$or": [{"change_rate": {"$gt": 9.9}}, {"change_rate": {"$lt": -9.9}}]}).sort('date', 1)
        aStock = []
        for i in res:
            del i['_id']
            aStock.append(i)

        # stop = stop + 1
        # if(stop == 20):
        #     saveCSV(results)
        #     return

        # print(aStock)

        window = []
        for i in range(1, len(aStock) - 3):
            if(find.nextTradingDay(aStock[i - 1]['date']) == aStock[i]['date']):
                if(len(window) == 2):
                    if(aStock[i]['change_rate'] < 0):
                        item = {'name': name['name'], 'symbol': name['symbol'], 'date': aStock[i - 2]['date']}
                        # item['d1'] = aStock[i - 2]['change_rate']
                        # item['d2'] = aStock[i - 1]['change_rate']
                        # item['d3'] = aStock[i]['change_rate']
                        item['d1'] = window[0]['change_rate']
                        item['d2'] = window[1]['change_rate']
                        item['d3'] = aStock[i]['change_rate']
                        d4 = quoteDao.find_one({'symbol': name['symbol'], 'date': find.nextTradingDay(aStock[i]['date'])})
                        if(d4 is not None):
                            item['d4'] = d4['change_rate']
                            d5 = quoteDao.find_one({'symbol': name['symbol'], 'date': find.nextTradingDay(d4['date'])})
                            if(d5 is not None):
                                item['d5'] = d5['change_rate']
                                d6 = quoteDao.find_one({'symbol': name['symbol'], 'date': find.nextTradingDay(d5['date'])})
                                if(d6 is not None):
                                    item['d6'] = d6['change_rate']
                                else:
                                    item['d6'] = 0.0
                            else:
                                item['d5'] = 0.0
                        else:
                            item['d4'] = 0.0
                        window.clear()
                        results.append(item)
                        # print(item)
                    else:
                        window.pop(0)
                        window.append(aStock[i])
                        # print('\rPattern Found:', len(results), end='')
                elif(len(window) < 2):
                    if(aStock[i]['change_rate'] > 0):
                        window.append(aStock[i])
                    else:
                        window.clear()
            else:
                window.clear()

        cnt = cnt + 1
        print('\rProgerss:', str(len(results)), format(cnt * 100 / total, '.2f') + '%', end='')
    saveCSV(results)


def saveCSV(data):
    df = pd.DataFrame.from_dict(data)
    df.to_csv('./snowball/shake.csv', encoding="utf_8_sig")
    print(len(data), 'items saved to CSV')


if __name__ == '__main__':
    findShakes()
