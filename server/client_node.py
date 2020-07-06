import _thread
import json
import socket
import sys
import time

import select

from common import db
from config import SERVER_IP, SERVER_PORT, DEF_REGIST, DEF_ADDBLOCK, DEF_DELAY

# 服务器处理函数
from model.block_model import dict2Block
from server.data_format import dict2DataFormat, DataFormat, DataFormat2dict

regist_status = -1  # 是否注册成功


# 客户端处理接收数据
def client_handl_rev(data):
    global regist_status
    d_format = json.loads(data, object_hook=dict2DataFormat)
    if d_format.dataType == DEF_REGIST:  # 节点注册成功，则开启服务
        if d_format.data == "OK":
            regist_status = 0
        else:
            regist_status = -1
    elif d_format.dataType == DEF_ADDBLOCK:  # 增加节点
        block = json.loads(d_format.data, object_hook=dict2Block)
        db.session.add(block)
        db.session.commit()
        print("添加区块成功")
    else:
        print("not support the format type：" + d_format.dataType)


# 节点服务器处理线程
def client_accept_process(client, port):
    while 1:
        try:
            data = str(client.recv(1024), encoding="utf-8")
            client_handl_rev(data)
        except Exception as err:
            print("断开连接！！" + str(sys._getframe().f_lineno) + " " + err)
            return


# 节点服务器
class ClientNode():
    def __init__(self):
        # 客户端 发送一个数据，再接收一个数据
        self.isOpen = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
        try:
            self.client.connect((SERVER_IP, SERVER_PORT))  # 建立一个链接，连接到本地的9090端口
            self.client.connect((SERVER_IP, SERVER_PORT))  # 建立一个链接，连接到本地的9090端口
        except Exception as err:
            print("Error: 连接不上服务器" + str(sys._getframe().f_lineno) + " " + str(err))

            return
        try:
            _thread.start_new_thread(client_accept_process, (self.client, SERVER_PORT))  # 创建侦听等待线程
        except Exception as err:
            print("Error: 无法启动线程" + str(sys._getframe().f_lineno) + " " + str(err))
        print("Creat Client Node successfully!!")
        self.isOpen = True

    # 发起注册请求
    def regesiter2server(self):
        if (self.isOpen == False):
            return -1
        global regist_status
        dataFormat = DataFormat("REGIST", "OK")
        json_str = json.dumps(dataFormat, default=DataFormat2dict)
        self.client.sendall(bytes(json_str, encoding="utf-8"))
        time.sleep(DEF_DELAY)
        return regist_status
