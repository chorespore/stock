import pymongo

client = pymongo.MongoClient(host='mongodb://working.chao.com', username='chao', password='mongo2020')
db = client["stock"]
quotes = db["price"]
names = db["name"]
snowballCol = db["snowball"]


def importSnowball(data):
    snowballCol.insert_many(data)
    print(len(data), 'Items importd to mongo')


def createIndex():
    indexes = ['symbol', 'date', 'percent']
    for idx in indexes:
        print('Creating index of', idx)
        snowballCol.create_index([(idx, 1)])
