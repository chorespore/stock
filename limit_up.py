import find
import datetime
from matplotlib import pyplot as plt

START = "2019-01-01"
PERIOD = 250
LIMIT_SPAN=15

tradingDays=[]

x = range(0, LIMIT_SPAN)
y = [0.0]*LIMIT_SPAN


def getTopSet(date):
    # query = {"date": date, "change_rate": {"$gt": 9.5, '$lt': 10.9}}
    query = {"date": date, "change_rate": {'$lt': 10.9}}
    res = find.priceColl.find(query).limit(100).sort('change_rate', -1)
    pool=set()
    for i in res:
        pool.add(i['symbol'])
    return pool

def getTopDict(start,period):
    global tradingDays
    topDict={}
    tradingDays=find.getTradingDays(start,period)
    for day in tradingDays:
        topDict[day]=getTopSet(day)
    return topDict

def draw():
    plt.title("Retrospective Diagram")
    plt.xlabel("Days")
    plt.ylabel("Ramining Rate")
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    # l = find.getTradingDays('2019-09-01',10)
    # print(l)
    statDict={}
    topDict=getTopDict(START,PERIOD)
    # print(topDict)
    # print(tradingDays)
    for day in tradingDays[:-LIMIT_SPAN]:
        remainedList=[]
        compareDays=find.getTradingDays(day,LIMIT_SPAN)
        for cmpDay in compareDays:
            topIntersection=topDict[day].intersection(topDict[cmpDay])
            remainedList.append(len(topIntersection))
        print(day,remainedList)
        statDict[day]=remainedList

    for day in tradingDays[:-LIMIT_SPAN]:
        remainedList=statDict[day]
        for i in range(LIMIT_SPAN):
            y[i]+=remainedList[i]
    
    y=[i/PERIOD for i in y]
    
    draw()



