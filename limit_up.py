import dao
import find
import datetime
from matplotlib import pyplot as plt

START = "2018-01-01"
PERIOD = 10


def getLimitedCount(date):
    query = {"date": date, "change_rate": {"$gt": -10.9, '$lt': -9.9}}
    resA = find.quoteDao.count_documents(query)
    query = {"date": date, "change_rate": {"$gt": -10.9, '$lt': -9.0}}
    resB = find.quoteDao.count_documents(query)
    # print(date, resA, resB, format(resA*100/resB, '.2f')+'%')
    print(date, resA, resB)
    return resA


def getLimited(date):
    query = {"date": date, "change_rate": {"$gt": -10.9, '$lt': -9.9}}
    resA = find.quoteDao.count_documents(query)
    query = {"date": date, "change_rate": {"$gt": -10.9, '$lt': -9.9}}
    resB = dao.quotes.find(query)
    print(date, resA, resB)
    for i in resB:
        d1 = dao.quotes.find_one({'date': find.getTradingDay(i['date'], 1), 'symbol': i['symbol']})
        d2 = dao.quotes.find_one({'date': find.getTradingDay(i['date'], 2), 'symbol': i['symbol']})
        d3 = dao.quotes.find_one({'date': find.getTradingDay(i['date'], 4), 'symbol': i['symbol']})
        if(d1 is not None and d2 is not None and d3 is not None):
            print(d1['change_rate'], d2['change_rate'], d3['change_rate'])

    # print(date, resA, resB, format(resA*100/resB, '.2f')+'%')
    return resA


if __name__ == '__main__':
    days = find.getTradingDays(START, PERIOD)
    x = range(0, PERIOD)
    y = []
    for d in days:
        y.append(getLimited(d))

    print('Average:', sum(y) / len(y))

    # find.draw(x, y)
