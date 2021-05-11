import dao
import find
import tools


def go(symbol):
    y = []
    capital = 100
    for stock in dao.quotes.find({'symbol': symbol, "date": {"$gt": '2018-01-01'}}).sort('date', 1):
        buyPoint = stock['open'] * (100 - 1.37) / 100
        nextDay = dao.quotes.find_one({'symbol': symbol, "date": find.nextTradingDay(stock['date'])})
        if nextDay is not None:
            sellPoint = nextDay['open'] * (100 + 1.5) / 100
            if stock['open'] < stock['high'] and stock['low'] < buyPoint:
                if nextDay['high'] > sellPoint:
                    capital = capital / buyPoint * sellPoint
                else:
                    capital = capital / buyPoint * nextDay['close']
                y.append(capital)
                print(len(y), capital)

    tools.drawY(y)


def openHigh(symbol):
    y = []
    for stock in dao.quotes.find({'symbol': symbol, "date": {"$gt": '2018-01-01'}}).sort('date', 1):
        y.append((stock['high'] - stock['open']) / stock['open'] * 100)
    # tools.drawY(y)
    if(len(y) > 0):
        res = sum(y) / len(y)
        # print(res)
        return res


def openLow(symbol):
    y = []
    for stock in dao.quotes.find({'symbol': symbol, "date": {"$gt": '2018-01-01'}}).sort('date', 1):
        y.append((stock['open'] - stock['low']) / stock['open'] * 100)
    # tools.drawY(y)
    if(len(y) > 0):
        res = sum(y) / len(y)
        # print(res)
        return res


def all():
    y = []
    for i in dao.names.find():
        amp = openLow(i['symbol'])
        if amp is not None:
            y.append(amp)
            print(len(y), y[-1])
    res = sum(y) / len(y)
    y.sort()
    print('Average:', res, 'Median:', y[int(len(y) / 2)], '90 percentile:', y[int(len(y) / 9)])
    tools.drawY(y)


if __name__ == '__main__':
    # all()
    go('SZ000002')
