import dao
import tools


def go(symbol):
    y = []
    for stock in dao.quotes.find({'symbol': symbol, "date": {"$gt": '2018-01-01'}}).sort('date', 1):
        y.append((stock['high'] - stock['low']) / stock['low'] * 100)
    # tools.drawY(y)
    if(len(y) > 0):
        res = sum(y) / len(y)
        # print(res)
        return res


def all():
    y = []
    for i in dao.names.find():
        amp = go(i['symbol'])
        if amp is not None:
            y.append(amp)
            print(len(y), y[-1])
    res = sum(y) / len(y)
    print(res)
    tools.drawY(y)


if __name__ == '__main__':
    all()
    # go('SZ000004')
