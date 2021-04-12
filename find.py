import pymongo

client = pymongo.MongoClient(host='mongodb://rock.chao.com', username='chao', password='mongo2020')
db = client["stock"]
collection = db["price"]

query = { "change_rate": { "$gt": 9.9} }
display={"symbol":1,"date":1,"change_rate":1}

res = collection.find(query,display).skip(0).limit(10)
for x in res:
  print(x)