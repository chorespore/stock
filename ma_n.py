import os
import dao
import find
import time
import tools

quoteDao = dao.quotes
nameDao = dao.names

START = "2018-01-01"
PERIOD = 8
COMMISSION = 2.5 / 10000
principal = 100.0
window = []

dayBoard = {}


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


def goOne(symbol):
    global dayBoard
    principal = 100.0
    serie = []

    y = []
    n = 6
    closeSum = 1
    highSum = 1
    res = quoteDao.find({'symbol': symbol}).sort('date', 1)
    for quote in res:
        item = {'symbol': symbol, 'date': quote['date'], 'close': quote['close'], 'high': quote['high']}
        if len(serie) > n:
            sum = quote['close']
            for i in range(1, n):
                sum = sum + serie[-i]['close']
            avg = sum / n
            item['ma5'] = avg
        else:
            item['ma5'] = quote['close']
        serie.append(item)

    cnt = 0
    passCnt = 0
    for i in range(1, len(serie) - 2):
        if (serie[i - 1]['close'] < serie[i - 1]['ma5'] and serie[i]['close'] > serie[i]['ma5']):
            cnt = cnt + 1
            if(dayBoard.__contains__(serie[i]['date']) == False):
                dayBoard[serie[i]['date']] = []
            dayBoard[serie[i]['date']].append(serie[i]['symbol'])
            if(serie[i]['close'] * 1.09 < serie[i + 1]['high']):
                principal = principal / serie[i]['close'] * serie[i]['close'] * 1.09 * (1 - COMMISSION)
                passCnt = passCnt + 1
            else:
                principal = principal / serie[i]['close'] * serie[i + 1]['close'] * (1 - COMMISSION)
            closeSum = closeSum + serie[i]['close']
            highSum = highSum + serie[i + 1]['high']
            # print(cnt, serie[i]['date'], serie[i]['close'], format(principal, '0.2f'))
            # print(serie)
            # y.append(principal)
    # print('Earnings:', principal)
    # find.draw(range(len(y)), y)
    # print(highSum, closeSum)
    return principal, cnt, highSum / closeSum


def goAll():
    stop = 0
    res = []
    data = []
    start = time.time()
    stocks = nameDao.find()
    total = nameDao.count_documents({})
    for stock in stocks:
        p, days, passCnt = goOne(stock['symbol'])
        # tools.showProgress(len(res), total, start)
        # print(stock['name'], p, end='\t')
        if days != 0:
            res.append(p)
            print(len(res), stock['name'], format(p, '0.2f'), passCnt, days)
            item = {'name': stock['name'], 'symbol': stock['symbol'], 'earning': format(p, '0.2f'), 'pass': passCnt, 'days': days}
            data.append(item)
        stop = stop + 1
        if stop > 1000:
            break
    tools.saveCSV(data, './snowball/ma5.csv')

    # dayData = []
    # for key, value in dayBoard.items():
    #     dayItem = {'date': key, 'number': len(value)}
    #     dayData.append(dayItem)
    # tools.saveCSV(dayData, './snowball/ma5-cnt.csv')

    return res


if __name__ == '__main__':
    arr = goAll()
    avg = sum(arr) / len(arr)
    print('Average Earnings:', format(avg / 100, '0.2f'), 'times')
    # goOne('SZ300390')
