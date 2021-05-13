import pymongo

client = pymongo.MongoClient(host='mongodb://working.chao.com', username='chao', password='mongo2020')
db = client["stock"]
quotes = db["price"]
names = db["name"]
snowball = db["snowball"]


def importSnowball(data):
    snowball.insert_many(data)
    print(len(data), 'Items importd to mongo')


def createIndex():
    indexes = ['symbol', 'date', 'percent']
    for idx in indexes:
        print('Creating index of', idx)
        snowball.create_index([(idx, 1)])


def deleteField():
    for stock in snowball.find({}):
        snowball.update({'_id': stock['_id']}, {'$unset': {'tick_size': 1, 'lot_size': 1, 'type': 1}})
