import datetime
import snowball
import database
import eastmoney

fieldMap = {'current': 'f2', 'percent': 'f3', 'change': 'f4', 'symbol': 'f12', 'name': 'f14',
            'high': 'f15', 'low': 'f16', 'open': 'f17', 'close': 'f18', 'pe': 'f23', 'pb_ttm': 'f115'}


def merge():
    data = []
    snowDict, eastDict = dict(), dict()
    snowData = snowball.fetch()
    eastData = eastmoney.fetch()

    # snowData = snowball.loadJson('./snowball/2021-04-19.json')
    # eastData = eastmoney.loadJson('./snowball/em2021-04-19.json')

    for i in snowData:
        snowDict[i['symbol'][2:]] = i

    for i in eastData:
        eastDict[i['f12']] = i

    common = set(snowDict.keys()).intersection(set(eastDict.keys()))

    for symbol in common:
        item = snowDict[symbol]
        item['high'] = eastDict[symbol][fieldMap['high']]
        item['low'] = eastDict[symbol][fieldMap['low']]
        item['open'] = eastDict[symbol][fieldMap['open']]
        item['close'] = eastDict[symbol][fieldMap['close']]
        item['date'] = str(datetime.datetime.now().date())
        data.append(item)

    snowball.saveJson(data)
    database.importSnowball(data)


if __name__ == '__main__':
    merge()
