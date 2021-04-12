import os
import csv
import time
import pymongo
import datetime
import pandas as pd

src = './allstock'
titles = ['symbol', 'date', 'open', 'high', 'low', 'close',
          'pre_close', 'change', 'change_rate', 'turnover', 'volume']
number_fields= set('')

client = pymongo.MongoClient(host='mongodb://rock.chao.com', username='chao', password='mongo2020')
# client = pymongo.MongoClient(host='mongodb://localhost', username='chao', password='mongo2020')
db = client["stock"]
collection = db["price"]

confirm = input("Delete databse y/n? \n")
if(confirm == 'y'):
    collection.delete_many({})

files = os.listdir(src)
total = 0
all_start=time.time()
for i, f in enumerate(files):
    # if(i > 1):
    #     exit()
    cnt = 0
    start=time.time()
    for line in open(os.path.join(src, f), encoding='utf-8'):
        # print(line)
        if(cnt==0):
            cnt += 1
            continue
        values = line.strip().split(',')
        item = {}
        for j, title in enumerate(titles):
            content=None
            if(title=='symbol'):
                content=values[j]
            elif(title=='date'):
                content=values[j]
            #     content=datetime.datetime(int(values[j][0:4]),int(values[j][4:6]),int(values[j][6:8]))
            else:
                content=float(values[j])
            item[title] = content
        collection.insert_one(item)
        cnt += 1
        total += 1
        if(total % 100 == 0):
            print(i, f, cnt,"speed:",int(cnt/(time.time()-start)))
    print(total)
    print('Time used:',time.time()-all_start)

print('Total size: ', collection.count_documents({}))
