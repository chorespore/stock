import pymongo
import datetime
import numpy as np 
from matplotlib import pyplot as plt  
# pip3 install matplotlib

start="2019-01-24"
end="2020-07-24"
period=200

principal=100.0
profit=0.0

x = np.arange(0,period) 
y=[]

client = pymongo.MongoClient(host='mongodb://rock.chao.com', username='chao', password='mongo2020')
db = client["stock"]
collection = db["price"]

display={"symbol":1,"date":1,"change_rate":1}

# res = collection.find(query,display).skip(0).limit(5).sort('change_rate',1)
# for x in res:
#   print(x)

def pick(date):
  query = { "date":date,"change_rate": { "$gt": 9.9},"change_rate": { "$lt": 11000.0} }
  res = collection.find(query).skip(0).limit(10).sort('change_rate',-1)
  return res[0]

def calc(start,period):
  global principal
  if(period>0):
    symbol=pick(preTradingDay(start))['symbol']
    todayPrice=collection.find_one({'symbol':symbol,'date':start})
    nextPrice=collection.find_one({'symbol':symbol,'date':nextTradingDay(start)})
    # print(todayPrice)
    # print(nextPrice)
    principal=principal/todayPrice['open']*nextPrice['close']
    print(principal)
    y.append(principal/100)
    calc(nextTradingDay(start),period-1)
  else:
    print('OK!')
    print(principal/100-1)


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
 
# a=pick('2020-08-07')
# print(a)
# print(a['symbol'])
# y=preTradingDay('2020-08-03')
# print('preTradingDay',str(y))
# y=nextTradingDay('2020-07-31')
# print('nextTradingDay',str(y))
calc(nextTradingDay(start),period)


plt.title("Matplotlib demo") 
plt.xlabel("x axis caption") 
plt.ylabel("y axis caption") 
plt.plot(x,y) 
plt.show()