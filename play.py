import dao


def go():
    res = dao.quotes.update_one({'symbol': 'SZ000002', 'date': '2039-03-04'}, {'$set': {'pe_ttm': 999.0}})
    # res = dao.quotes.find({'symbol': 'SZ000002', 'date': '2019-03-04'}).explain()
    print(res.matched_count, res.modified_count)


if __name__ == '__main__':
    go()
