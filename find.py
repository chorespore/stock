import pymongo
import datetime
import numpy as np 
from matplotlib import pyplot as plt  
# pip3 install matplotlib

start="2017-01-24"
end="2020-07-24"
PERIOD=250

principal=100.0
profit=0.0

x = np.arange(0,PERIOD) 
y=[]

client = pymongo.MongoClient(host='mongodb://localhost', username='chao', password='mongo2020')
db = client["stock"]
collection = db["price"]

display={"symbol":1,"date":1,"change_rate":1}

def pick(date):
  query = { "date":date,"change_rate": { "$gt": 9.9},"change_rate": { "$lt": 2000.0} }
  res = collection.find(query).skip(0).limit(10).sort('change_rate',-1)
  return res[0]

def calc(start,period):
  global principal,PERIOD
  if(period>0):
    prePrice=pick(preTradingDay(start))
    symbol=prePrice['symbol']
    todayPrice=collection.find_one({'symbol':symbol,'date':start})
    nextPrice=collection.find_one({'symbol':symbol,'date':nextTradingDay(start)})
    # print(nextPrice)
    principal=principal/todayPrice['open']*nextPrice['close']
    print(PERIOD-period,end='\t')
    print(format(prePrice['change_rate'],'.2f'),end='\t')
    print(format(todayPrice['change_rate'],'.2f'),end='\t')
    print(format(nextPrice['change_rate'],'.2f'),end='\t')
    print(format(principal,'.2f'))
    y.append(principal/100)
    calc(nextTradingDay(start),period-1)

def getDay(today,offset): 
    today=datetime.datetime.strptime(today, '%Y-%m-%d').date()
    span=datetime.timedelta(days=offset)
    res=str(today+span)  
    return res

def preTradingDay(today): 
    for i in range(1,90):
      target=getDay(today,-i)
      count = collection.count_documents({ "date":target })
      if(count>0):
        return target

def nextTradingDay(today): 
    for i in range(1,90):
      target=getDay(today,i)
      count = collection.count_documents({ "date":target })
      if(count>0):
        return target
 
calc(nextTradingDay(start),PERIOD)
print('\nEarnings of',PERIOD, 'days:',format(principal/100-1,'.2f'),'times')

plt.title("Retrospective Diagram") 
plt.xlabel("Days") 
plt.ylabel("Returns") 
plt.plot(x,y) 
plt.show()