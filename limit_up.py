import find
import find
import datetime
from matplotlib import pyplot as plt

START = "2018-01-01"
PERIOD = 500


def getLimitedCount(date):
    query = {"date": date, "change_rate": {"$gt": 9.9, '$lt': 10.9}}
    resA = find.priceColl.count_documents(query)
    query = {"date": date, "change_rate": {"$gt": 9.0, '$lt': 10.9}}
    resB = find.priceColl.count_documents(query)
    print(date, resA, resB, format(resA*100/resB, '.2f')+'%')
    return resA


if __name__ == '__main__':
    days = find.getTradingDays(START, PERIOD)
    x = range(0, PERIOD)
    y = []
    for d in days:
        y.append(getLimitedCount(d))

    print('Average:', sum(y)/len(y))

    find.draw(x, y)
