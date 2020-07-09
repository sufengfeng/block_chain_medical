# config=utf-8
import _thread
import copy
import json
import sys
import time
from argparse import ArgumentParser

from common import db
from config import DEF_ADDBLOCK
from login import userRoute
from model import create_app, Block
from flask_login import login_user
from flask import render_template, request, redirect

from model.record_model import Record
from model.user_model import User
from server.client_node import ClientNode
from server.client_node import current_block

DEFAULT_MODULES = [userRoute]
user = User()
app = create_app('../config.py')

for module in DEFAULT_MODULES:
    app.register_blueprint(module)


# 增加区块
def add_Block(patient, describe):
    global user
    global current_block
    timestamp = time.time()

    block = Block(timestamp=timestamp, doctor=user.name, patient=patient, describe=describe)
    block.index = int(current_block.index) + 1
    block.encryption = str(hash(current_block))  # 同态加密
    db.session.add(block)
    db.session.commit()
    ClientNode.send_ADDBLOCK_message(block)
    current_block = copy.deepcopy(block)  # 更新当前block数据


# 查找
def get_all_blocks():
    block = Block.query.filter()
    blocks = block.all()
    # print(blocks)
    return blocks


record = Record()


def update_record(index, describe):
    block = Block.query.filter(Block.index == index).first()
    record = Record()
    record.timestamp = time.time()
    record.pre_describe = block.describe
    record.describe = describe

    db.session.add(record)
    db.session.commit()
    pass


# 更新
def update_Block(index, describe):
    update_record(index, describe)
    Block.query.filter(Block.index == index).update({Block.describe: describe})
    db.session.commit()


@app.before_request
def before_request():
    pass


@app.route('/init')
def init():
    db.create_all()
    return 'ok'


@app.route('/', endpoint="/")
@app.route('/index', endpoint="index", )
def index():
    if user.name == "anonymous":
        user.name = "Sign in"
    blocks = get_all_blocks()
    return render_template('index.html', user=user, blocks=blocks)


@app.route('/product', endpoint="product")
def product():
    return render_template('product.html')


@app.route('/about-us', endpoint="about-us")
def about():
    return render_template('about-us.html', user=user)


@app.route('/feature', endpoint="feature")
def feature():
    return render_template('feature.html')


@app.route('/team', endpoint="team")
def team():
    return render_template('team.html')


@app.route('/update', endpoint="update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        print(request.form.get("id"))
        block = Block.query.filter(Block.index == request.form.get("id")).first()
        if block:
            return render_template('update.html', user=user, block=block)
        else:
            return redirect("/")
    if request.method == 'GET':
        block = Block.query.filter(User.user_id == 1).first()
        if block:
            return render_template('update.html', user=user, block=block)
        else:
            return redirect("/")
    return redirect("/")


@app.route('/contact', endpoint="contact")
def contact():
    return render_template('contact.html')


@app.route('/404-error', endpoint="404-error")
def error():
    return render_template('404-error.html')


@app.route('/coming-soon', endpoint="coming-soon")
def coming():
    return render_template('coming-soon.html')


@app.route('/blog', endpoint="blog")
def blog():
    return render_template('blog.html')


@app.route('/get-started', endpoint="get-started")
def started():
    global user
    user = User()
    return render_template('get-started.html')


@app.route('/login', endpoint="login", methods=['GET', 'POST'])
def login():
    global user
    if request.method == 'POST':
        user = User.query.filter(User.name == request.form.get("yourname"),
                                 User.password == request.form.get("yourpw")).first()
        if user:
            login_user(user)
            return redirect('/')
        else:
            user = User()
    return render_template('get-started.html')


@app.route('/add_block', endpoint="add_block", methods=['GET', 'POST'])
def add_block():
    global user
    if user.role == "doctor":
        if request.method == 'POST':
            params = json.loads(request.data)
            add_Block(params["patient"], params["describe"])
            respone = {"errno": 200, "message": "Add block Success!!"}
            data = json.dumps(respone)
            return data, 200, {"ContentType": "application/json"}
    respone = {"errno": 200, "message": "Only the doctor could add block"}
    data = json.dumps(respone)
    return data, 200, {"ContentType": "application/json"}


@app.route('/updateblock', endpoint="updateblock", methods=['GET', 'POST'])
def updateblock():
    global user
    index = 1
    describe = ""
    if user.role == "doctor":
        if request.method == 'POST':
            params = json.loads(request.data)
            index = params["index"]
            describe = params["describe"]
            update_Block(index, describe)
            respone = {"errno": 200, "message": "update block Success!!"}
            data = json.dumps(respone)
            return data, 200, {"ContentType": "application/json"}
    respone = {"errno": 200, "message": "Only the doctor could update block"}
    data = json.dumps(respone)
    return data, 200, {"ContentType": "application/json"}


@app.route('/regist', endpoint="regist", methods=['GET', 'POST'])
def regist():
    global user
    if request.method == 'POST':
        if user.role != "admin":
            respone = {"errno": 200, "message": "Only the admin could add users"}
            data = json.dumps(respone)
            return data, 200, {"ContentType": "application/json"}
        params = json.loads(request.data)
        user_add = User()
        user_add.name = params["name"]
        user_add.password = params["password"]
        user_add.role = params["role"]
        db.session.add(user_add)
        db.session.commit()
        respone = {"errno": 200, "message": "creat user Success!!"}
        data = json.dumps(respone)
        return data, 200, {"ContentType": "application/json"}

    if request.method == 'GET':
        return render_template('regist.html', user=user)
    return render_template("404-error.html")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5050, type=int, help='port to listen on')  # 端口

    args = parser.parse_args()
    port = args.port

    client = ClientNode()
    if (client == None):
        print("创建节点服务器失败！！")
        exit(-1)
    ret = client.regesiter2server()
    if ret == 0:
        print("注册成功，节点正常运行！！")
        app.run(debug=True, host='127.0.0.1', port=port)
    else:
        print("服务器注册出错，开启中央服务器，并尝试再次连接！！")
