import os
import csv
import time
import pymongo
import pandas as pd

src = './allstock'
titles = ['symbol', 'date', 'open', 'high', 'low', 'close',
          'pre_close', 'change', 'change_rate', 'turnover', 'volume']

client = pymongo.MongoClient(host='mongodb://rock.chao.com', username='chao', password='mongo2020')
db = client["stock"]
collection = db["price"]
collection.delete_many({})

files = os.listdir(src)
size = len(files)
print(size)
total = 0
time_start=time.time()
for i, f in enumerate(files):
    # if(i > 1):
    #     exit()
    cnt = 0
    for line in open(os.path.join(src, f), encoding='utf-8'):
        # print(line)
        if(cnt==0):
            cnt += 1
            continue
        values = line.strip().split(',')
        item = {}
        for j, title in enumerate(titles):
            item[title] = values[j]
        collection.insert_one(item)
        cnt += 1
        total += 1
        if(total % 200 == 0):
            time_used=time.time()-time_start
            print(i, f, cnt,'speed:',int(total/(time_used)))
    print(total)
    print('Tiem used:',time_used,'s')

# for x in collection.find():
#     print(x)

print('Total size: ', collection.count_documents({}))
