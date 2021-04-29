import dao
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from bson import json_util

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def hello_world():
    return 'Hello Flask'


@app.route('/quote/<symbol>', methods=['GET'])
def quote(symbol):
    data = []
    res = dao.quotes.find({'symbol': symbol}).sort('date', 1)
    for i in res:
        data.append(i)
    return json_util.dumps(data)


@app.route('/stock', methods=['GET'])
def stock():
    res = None
    data = []
    keyword = request.args.get('keyword')
    if keyword is None:
        res = dao.names.find({})
    else:
        res = dao.names.find({'keyword': {'$regex': keyword.lower()}}).sort('symbol', 1)
    for i in res:
        del i['_id']
        del i['keyword']
        data.append(i)
    return json_util.dumps(data)


@ app.route('/listAll', methods=['GET'])
def listAll():
    data = []
    res = dao.names.find({}).sort('symbol', 1)
    for i in res:
        del i['_id']
        data.append(i)
    return json_util.dumps(data)


@ app.route('/student', methods=['POST'])
def add_stu():
    if not request.data:  # 检测是否有数据
        return ('fail')
    student = request.data.decode('utf-8')
    student_json = json.loads(student)
    return request.data


if __name__ == '__main__':
    app.run(port=8086, debug=True)
