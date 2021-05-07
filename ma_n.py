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
        if (serie[i - 1]['close'] < serie[i - 1]['ma5'] and serie[i]['close'] > serie[i]['ma5'] and serie[i]['close'] < serie[i]['high']):
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
        if stop > 5000:
            break
    tools.saveCSV(data, './snowball/ma5.csv')

    # dayData = []
    # for key, value in dayBoard.items():
    #     dayItem = {'date': key, 'number': len(value)}
    #     dayData.append(dayItem)
    # tools.saveCSV(dayData, './snowball/ma5-cnt.csv')
    avg = sum(res) / len(res)
    print('Average Earnings:', format(avg / 100, '0.2f'), 'times')
    return res


def searchDay(today):
    res = []
    MA_N = 6
    days = []
    for i in range(1, MA_N + 1):
        days.append(find.getTradingDay(today, -i))
    # print(days)
    for i in quoteDao.find({'date': today}):
        preDays = []
        for j in quoteDao.find({'symbol': i['symbol'], 'date': {'$in': days}}).sort('date', -1):
            preDays.append(j)
        if(len(preDays) < 5):
            continue
        avg = sum(list(map(lambda x: x['close'], preDays))) / len(preDays)
        if(preDays[0]['close'] < avg and i['close'] > avg and i['close'] < i['high']):
            nextDay = quoteDao.find_one({'symbol': i['symbol'], 'date': find.nextTradingDay(today)})
            if nextDay is not None:
                pe = 999
                if i.__contains__('pe_ttm'):
                    pe = i['pe_ttm']
                # if pe > 0 and pe < 50:
                item = {'symbol': i['symbol'], 'ma': avg, 'pe_ttm': pe, 'close': i['close'], 'nextDay': nextDay['close'], 'earnings': nextDay['close'] / i['close'] * 100 - 100}
            else:
                continue
            # print(item)
            res.append(item)
    # res.sort(key=lambda x: x['pe_ttm'])
    # res = res[:20]
    # tools.saveCSV(res[:10], './snowball/searchDay.csv')
    # print(res)
    return sum(list(map(lambda x: x['earnings'], res))) / len(res)


def search():
    P = 100
    days = []
    y = []
    start = '2018-06-01'
    for i in range(1, 250 + 1):
        start = find.nextTradingDay(start)
        days.append(start)
        change = searchDay(start)
        P = P * ((100 + change) / 100) * 9995 / 10000
        print(i, change, P)
        y.append(P)

    find.draw(range(len(y)), y)


if __name__ == '__main__':
    goAll()
    # e = searchDay(find.nextTradingDay('2020-05-19'))
    # print(e)
    # goOne('SZ300688')
