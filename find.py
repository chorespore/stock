import pymongo
import datetime

client = pymongo.MongoClient(host='mongodb://rock.chao.com', username='chao', password='mongo2020')
db = client["stock"]
collection = db["price"]

query = { "date":"2020-07-24","change_rate": { "$gt": 9.9} }
display={"symbol":1,"date":1,"change_rate":1}

res = collection.find(query,display).skip(0).limit(1)
for x in res:
  print(x)

def getDay(current,offset): 
    today=datetime.datetime.strptime(current, '%Y-%m-%d').date()
    oneday=datetime.timedelta(days=offset)
    yesterday=today+oneday  
    return yesterday
 
y=getDay('2020-08-07',-20)
print('str',str(y))