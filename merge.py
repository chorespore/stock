import eastmoney
import snowball


if __name__ == '__main__':
    # snowData = snowball.fetch()
    # eastData = eastmoney.fetch()
    snowDict, eastDict = dict(), dict()

    snowData = snowball.loadJson('./snowball/2021-04-20.json')
    eastData = eastmoney.loadJson('./snowball/em2021-04-20.json')

    for i in snowData:
        snowDict[i['symbol'][2:]] = i

    for i in eastData:
        eastDict[i['f12']] = i

    print(snowDict.keys())
    print(eastDict.keys())
