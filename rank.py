import dao
import tools


def go(symbol):
    output = []
    x, y = [], []
    days = dao.quotes.find({'symbol': symbol}).sort('date', 1)
    for day in days:
        # print(day)

        stocks = dao.quotes.find({'date': day['date']}, {'symbol': 1}).sort('change_rate', -1)
        cnt = 0
        for stock in stocks:
            cnt = cnt + 1
            if(symbol == stock['symbol']):
                break
        total = dao.quotes.count_documents({'date': day['date']})
        print(cnt, format(cnt / total * 100, '.2f'))
        x.append(day['date'])
        y.append(1 - cnt / total)
        item = [day['date'], day['open'], day['close'], day['low'], day['high'], 1 - cnt / total]
        output.append(item)

    tools.saveJson(output, 'rank.json')
    tools.drawXY(x, y)


if __name__ == '__main__':
    go('SZ002594')
