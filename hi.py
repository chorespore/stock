import dao
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from bson import json_util

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/quote/<symbol>', methods=['GET'])
def quote(symbol):
    data = []
    res = dao.quotes.find({'symbol': symbol}).sort('date', 1)
    for i in res:
        data.append(i)
    return json_util.dumps(data)


@app.route('/stock/<keyword>', methods=['GET'])
def stock(keyword):
    data = []
    res = dao.names.find({'symbol': keyword})
    for i in res:
        data.append(i)
    return json_util.dumps(data)


@app.route('/listAll', methods=['GET'])
def listAll():
    data = []
    res = dao.names.find({})
    for i in res:
        data.append(i)
    return json_util.dumps(data)


@app.route('/student', methods=['POST', 'GET'])
def add_stu():
    if not request.data:  # 检测是否有数据
        return ('fail')
    student = request.data.decode('utf-8')
    student_json = json.loads(student)
    return request.data


if __name__ == '__main__':
    app.run(port=8086, debug=True)
