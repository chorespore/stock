import os
import csv
import time
import pymongo
import datetime
import pandas as pd

src = './allstock'
titles = ['symbol', 'date', 'open', 'high', 'low', 'close',
          'pre_close', 'change', 'change_rate', 'turnover', 'volume']

# client = pymongo.MongoClient(host='mongodb://rock.chao.com', username='chao', password='mongo2020')
client = pymongo.MongoClient(
    host='mongodb://localhost', username='chao', password='mongo2020')
db = client["stock"]
collection = db["price"]

confirm = input("Delete databse y/n? \n")
if(confirm == 'y'):
    collection.delete_many({})

total = 0
all_start = time.time()
files = os.listdir(src)

N = 0
for f in files:
    N = N+len(open(os.path.join(src, f), encoding='utf-8').readlines())
print(N, 'lines to insert')

for i, f in enumerate(files):
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
        collection.insert_one(item)
        cnt += 1
        total += 1
        if(total % 1000 == 0):
            print(i, f, cnt, "speed:", int(cnt/(time.time()-start)))
    print(str(total) + '/' + str(N), str(format(total/N, '.3f'))+'%')
    print('Time used:', str(int(time.time()-all_start)) + 's')

print('Total size: ', collection.count_documents({}))
