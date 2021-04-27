import dao
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/data/<symbol>', methods=['POST', 'GET'])
def data(symbol):
    data = []
    res = dao.names.find({'symbol': symbol})
    return res[0]


@app.route('/student', methods=['post'])
def add_stu():
    if not request.data:  # 检测是否有数据
        return ('fail')
    student = request.data.decode('utf-8')
    student_json = json.loads(student)
    return request.data


if __name__ == '__main__':
    app.run(port=8086, debug=True)
