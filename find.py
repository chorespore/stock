import dao
import pymongo
import datetime
from matplotlib import pyplot as plt

start = "2018-01-01"
PERIOD = 10
COMMISSION = 2.5 / 10000

principal = 100.0

x = range(PERIOD)
y = []

quoteDao = dao.quotes
nameDao = dao.names

display = {"symbol": 1, "date": 1, "change_rate": 1}


def pick(date):
    query = {"date": date, "change_rate": {"$gt": 9.9, "$lt": 1000.5}}
    res = quoteDao.find(query).skip(0).limit(10).sort('change_rate', -1)
    return res[0]


def calc(start, period):
    global principal, PERIOD
    if(period > 0):
        prePrice = pick(preTradingDay(start))
        symbol = prePrice['symbol']
        todayPrice = quoteDao.find_one({'symbol': symbol, 'date': start})
        nextPrice = quoteDao.find_one({'symbol': symbol, 'date': nextTradingDay(start)})
        if(todayPrice is None or nextPrice is None):
            print('-----------------------------------------------------')
            y.append(principal / 100)
            calc(nextTradingDay(start), period - 1)
            return
        principal = principal * (1 - COMMISSION) / todayPrice['open'] * nextPrice['close']
        y.append(principal / 100)
        name = '一一一一'
        nameRes = nameDao.find_one({'symbol': symbol})
        if(nameRes is not None):
            name = nameRes['name']

        print(PERIOD - period, end='\t')
        print(name.ljust(6, ' '), end='\t')
        print(todayPrice['date'], end='\t')
        print(format(prePrice['change_rate'], '.2f'), end='\t')
        print(format(todayPrice['change_rate'], '.2f'), end='\t')
        print(format(nextPrice['change_rate'], '.2f'), end='\t')
        print(format(principal, '.2f'))

        calc(nextTradingDay(start), period - 1)
    else:
        print('\nEarnings of', PERIOD, 'days:', format(principal / 100 - 1, '.2f'), 'times')
        drawEx()


def getTradingDays(start, period):
    tradingDays = []
    for i in range(period):
        day = nextTradingDay(start)
        tradingDays.append(day)
        start = day
    return tradingDays


def getDay(today, offset):
    today = datetime.datetime.strptime(today, '%Y-%m-%d').date()
    span = datetime.timedelta(days=offset)
    res = str(today + span)
    return res


def preTradingDay(today):
    for i in range(1, 90):
        target = getDay(today, -i)
        count = quoteDao.count_documents({"date": target})
        if(count > 0):
            return target


def nextTradingDay(today):
    for i in range(1, 90):
        target = getDay(today, i)
        count = quoteDao.count_documents({"date": target})
        if(count > 0):
            return target


def getTradingDay(today, offset):
    if offset >= 0:
        for i in range(offset):
            today = nextTradingDay(today)
    else:
        for i in range(-offset):
            today = preTradingDay(today)
    return today


def drawEx():
    plt.title("Retrospective Diagram")
    plt.xlabel("Days")
    plt.ylabel("Returns")
    plt.plot(x, y)
    plt.show()


def draw(x, y):
    plt.title("Retrospective Diagram")
    plt.xlabel("Days")
    plt.ylabel("Count")
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    calc(nextTradingDay(start), PERIOD)
