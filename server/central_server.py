# config=utf-8
import _thread
import json
import socket
import sys
import select
import time
from common import db
from config import SERVER_PORT, DEF_REGIST, DEF_ADDBLOCK
from server.data_format import dict2DataFormat, DataFormat2dict, DataFormat
from server.server_block_model import dict2BlockS, BlockS, BlockS2dict


# 向新注册节点发送现有的区块链数据
def send_all_block(client):
    blockServer_quer = BlockS.query.filter()
    blockServers = blockServer_quer.all()
    print(blockServers)
    for block in blockServers:
        json_str = json.dumps(block, default=BlockS2dict)
        dataFormat = DataFormat(DEF_ADDBLOCK, json_str)
        sendData = json.dumps(dataFormat, default=DataFormat2dict)
        try:
            client.sendall(bytes(sendData, encoding="utf-8"))
        except Exception as ex:
            print("Error: 发送错误" + str(sys._getframe().f_lineno) + " " + err)
            return


# 服务器端处理数据
def server_handl_rev(inpu, sk1, sk, data):
    d_format = json.loads(data, object_hook=dict2DataFormat)
    if d_format.dataType == DEF_REGIST:  # 设备节点
        send_all_block(sk)  # 更新区块链到子节点
        dataFormat = DataFormat(DEF_REGIST, "OK")
        json_str = json.dumps(dataFormat, default=DataFormat2dict)
        sk.sendall(bytes(json_str, encoding="utf-8"))
    elif d_format.dataType == DEF_ADDBLOCK:  # 增加节点
        # 增加中央服务器节点
        blockS = json.loads(d_format.data, object_hook=dict2BlockS)
        db.session.add(blockS)
        db.session.commit()
        # 发送添加区块到所有节点
        for client in inpu:
            if client == sk1:  # 不发送给自身
                continue
            client.sendall(bytes(data, encoding="utf-8"))
            client.send()


# 中央服务器接收处理线程
def server_accept_process(sk1, port):
    inpu = [sk1, ]
    while True:
        r_list, w_list, e_list = select.select(inpu, [], [], 1)
        for sk in r_list:
            if sk == sk1:
                conn, address = sk.accept()
                inpu.append(conn)
            else:
                try:
                    data = str(sk.recv(1024), encoding="utf-8")
                    server_handl_rev(inpu, sk1, sk, data)
                except Exception as ex:
                    inpu.remove(sk)


def add_first_block():
    timestamp = time.time()
    block = BlockS(timestamp=timestamp, doctor="admin", patient="patient", describe="None")
    block.encryption = hash(block)  # 同态加密
    db.session.add(block)
    db.session.commit()


# 中央服务器
class CentralServer():
    def __init__(self):
        sk1 = socket.socket()
        sk1.bind(("127.0.0.1", 2248))
        sk1.listen()
        try:
            _thread.start_new_thread(server_accept_process, (sk1, SERVER_PORT))  # 创建侦听等待线程
        except Exception as err:
            print("Error: 无法启动线程" + str(sys._getframe().f_lineno) + " " + err)
        add_first_block()  # 添加首节点
        print("Creat Central Server successfully!!")


if __name__ == '__main__':
    server = CentralServer()  # 创建中心服务器
    # 创建两个线程
    try:
        # _thread.start_new_thread(client_test, ("Thread-1", 1,))
        # _thread.start_new_thread(client_test, ("Thread-2", 2,))
        # _thread.start_new_thread(client_test, ("Thread-3", 3,))
        # _thread.start_new_thread(client_test, ("Thread-4", 4,))
        pass
    except Exception as err:
        print("Error: 无法启动线程" + str(sys._getframe().f_lineno) + " " + err)
    while 1:
        pass
