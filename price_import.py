import os
import csv
import time
import pymongo
import datetime
import pandas as pd

src = './allstock'
titles = ['symbol', 'date', 'open', 'high', 'low', 'close',
          'pre_close', 'change', 'change_rate', 'turnover', 'volume']

client = pymongo.MongoClient(host='mongodb://localhost', username='chao', password='mongo2020')
db = client["stock"]
priceColl = db["price"]

def importData():
    confirm = input("Delete database y/n ? \n")
    if(confirm == 'y'):
        priceColl.drop()

    total = 0
    all_start = time.time()
    files = os.listdir(src)

    N = 0
    for f in files:
        N = N+len(open(os.path.join(src, f), encoding='utf-8').readlines())
    print(N, 'lines to insert')

    for i, f in enumerate(files):
        print(i, f, end=' ')
        cnt = 0
        start = time.time()
        for line in open(os.path.join(src, f), encoding='utf-8'):
            if(cnt == 0):
                cnt += 1
                continue
            values = line.strip().split(',')
            item = {}
            for j, title in enumerate(titles):
                content = None
                if(title == 'symbol'):
                    content = values[j]
                elif(title == 'date'):
                    day = datetime.datetime.strptime(values[j], '%Y%m%d').date()
                    content = str(day)
                #     content=datetime.datetime(int(values[j][0:4]),int(values[j][4:6]),int(values[j][6:8]))
                else:
                    content = float(values[j])
                item[title] = content
            priceColl.insert_one(item)
            cnt += 1
            total += 1
            if(total % 100 == 0):
                print('|', end='', flush=True)
        print(" Speed:", int(cnt/(time.time()-start)), end='')
        timeUsed = int(time.time()-all_start)
        print('  Progress:', str(total) + '/' + str(N),str(format(total/N*100, '.3f'))+'%')
        print('Time used:', str(timeUsed) + 's', end='  ')
        print('Time estimated:', str(format(timeUsed*N/total/3600, '.2f'))+'h', end='  ')
        print('Time remaining:', str(format((timeUsed*N/total-timeUsed)/3600, '.2f'))+'h')
    print('Total size: ', priceColl.count_documents({}))

def createIndex():
    indexes=['symbol','date','change_rate']
    for idx in indexes:
        print('Creating index of',idx)
        priceColl.create_index([(idx,1)])

def updateSymbol():
    symbolSet=set()
    res=priceColl.find()
    for i in res:
        s=i['symbol']
        if(s not in symbolSet and '.' in s):
            symbolSet.add(s)
            parts=s.split('.')
            print(s,parts[1]+parts[0])
            priceColl.update_many({'symbol':s},{"$set":{"symbol":parts[1]+parts[0]}})
    print(len(symbolSet))

# importData()
# createIndex()
updateSymbol()
