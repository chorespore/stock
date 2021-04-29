import os
import dao
import find
import tools

quoteDao = dao.quotes
nameDao = dao.names

start = "2018-01-01"
PERIOD = 250
COMMISSION = 2.5 / 10000


def preLoad():
    results = []
    cnt = 0
    total = nameDao.count_documents({})
    print('Items to search:', total)
    for name in nameDao.find():


if __name__ == '__main__':
    # merge()
    # getPE('SH601318')
    preLoad()
