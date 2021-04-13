import pymongo
import datetime

client = pymongo.MongoClient(host='mongodb://rock.chao.com', username='chao', password='mongo2020')
db = client["stock"]
collection = db["price"]

start="2019-07-24"
period=100
end="2020-07-24"
profit=0.0

query = { "date":"2020-07-24","change_rate": { "$gt": 10} }
display={"symbol":1,"date":1,"change_rate":1}

# res = collection.find(query,display).skip(0).limit(5).sort('change_rate',1)
# for x in res:
#   print(x)

def pick(date):
  query = { "date":date,"change_rate": { "$gt": 10} }
  res = collection.find(query).skip(0).limit(5).sort('change_rate',1)
  return res[0]

def calc():
  for i in range(period):
    today=getDay(start,i)


def getDay(current,offset): 
    today=datetime.datetime.strptime(current, '%Y-%m-%d').date()
    span=datetime.timedelta(days=offset)
    res=str(today+span)  
    return res
 
a=pick('2020-08-07')
print(a)
print(a['symbol'])
# y=getDay('2020-08-07',-20)
# print('str',str(y))