import os
import dao
import find
import tools

quoteDao = dao.quotes
nameDao = dao.names

START = "2018-01-01"
PERIOD = 8
COMMISSION = 2.5 / 10000
principal = 100.0
window = []


def go(start, period):
    global principal, PERIOD, window
    if period > 0:
        if len(window) < 6:
            oneDay = {}
            res = quoteDao.find({'date': start})
            for quote in res:
                oneDay[quote['symbol']] = quote['close']
            window.append(oneDay)
        else:
            print(window)
        go(find.nextTradingDay(start), period - 1)


def goOne():
    global principal
    serie = []
    window = []
    n = 5
    res = quoteDao.find({'symbol': 'SZ000006'}).sort('date', 1)
    for quote in res:
        item = {'date': quote['date'], 'close': quote['close']}
        if len(serie) > 5:
            sum = quote['close']
            for i in range(1, n):
                sum = sum + serie[-i]['close']
            avg = sum / n
            item['ma5'] = avg
        else:
            item['ma5'] = quote['close']
        serie.append(item)

    cnt = 0
    for i in range(1, len(serie) - 1):
        if (serie[i - 1]['close'] < serie[i - 1]['ma5'] and serie[i]['close'] > serie[i]['ma5']):
            cnt = cnt + 1
            print(cnt, serie[i]['date'], serie[i]['close'], serie[i]['ma5'])
            principal = principal / serie[i]['close'] * serie[i + 1]['close']
            # print(serie)
    print(principal)


if __name__ == '__main__':
    goOne()
