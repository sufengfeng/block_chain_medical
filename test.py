# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import json
from argparse import ArgumentParser




from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# # 维护连接
# def link_hadle_process(conn, addr):
#     print(addr)
#     while 1:
#         try:
#             data = conn.recv(1024)  # 接收数据，data是byte类型
#         except Exception as err:
#             # print(sys._getframe().f_lineno)
#             print(err)
#             print(addr)
#             return
#         print('recive:', data.decode())  # 打印接收到的数据
#         conn.sendall('收到请求'.encode('utf-8'))  # 发送数据
#
#
# # 侦听新的连接
# def server_accept_process(server, port):
#     while (1):
#         conn, addr = server.accept()
#         try:
#             _thread.start_new_thread(link_hadle_process, (conn, addr))  # 创建侦听等待线程
#         except Exception as err:
#             print('无法启动线程' + ' ,File: "' + __file__ + '", Line ' + str(
#                 sys._getframe().f_lineno) + ' , in ' + sys._getframe().f_code.co_name + ' error: ' + err)
#
#
# # 中心服务器
# class CentralServer():
#     def __init__(self):
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个socket
#         server.bind((SERVER_IP, SERVER_PORT))  # 将socket绑定到监听的端口
#         server.listen()
#         try:
#             _thread.start_new_thread(server_accept_process, (server, SERVER_PORT))  # 创建侦听等待线程
#         except Exception as err:
#             print("Error: 无法启动线程" + str(sys._getframe().f_lineno) + " " + err)
#         print("Creat Central Server successfully!!")
#         print("Creat Central Server successfully!!")
#
# if __name__ == '__main__':
#     parser = ArgumentParser()
#     parser.add_argument('-p', '--port', default=5050, type=int, help='port to listen on')
#     parser.add_argument('-r', '--sRun', default=0, type=int, help='central server on')
#     args = parser.parse_args()
#     port = args.port
#     sRun=args.sRun
#     print(port,sRun)

#
# class BlockS():
#     # __tablename__ = 'tb_blocks'
#     # index = db.Column(db.Integer, primary_key=True)
#     # timestamp = db.Column(db.String(200), nullable=False)  # 时间戳
#     #
#     # doctor = db.Column(db.String(200), nullable=False)  # 区块拥有者
#     # patient = db.Column(db.String(200), nullable=False)  # 区块描述对象
#     # describe = db.Column(db.String(200), nullable=False)  # 描述
#     #
#     # proof = db.Column(db.String(200), nullable=False)  # 证明 无
#     # encryption = db.Column(db.String(200), nullable=False)  # 同态加密
#
#     def __init__(self, index=None, timestamp=None, doctor=None, patient="anonymous", describe=None, proof="proof",
#                  encryption="previous_hash"):
#         self.index = index
#         self.timestamp = timestamp
#
#         self.doctor = doctor
#         self.patient = patient
#         self.describe = describe
#
#         self.proof = proof
#         self.encryption = encryption
#
#     @staticmethod
#     def hash(block):
#         """
#         Creates a SHA-256 hash of a Block
#
#         :param block: Block
#         """
#
#         # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
#         block_string = json.dumps(block, sort_keys=True).encode()
#         return hashlib.sha256(block_string).hexdigest()
#
#
# def BlockS2dict(data):
#     return {
#     'index': data.index,
#     'timestamp': data.timestamp,
#     'doctor': data.doctor,
#     'patient': data.patient,
#     'describe': data.describe,
#
#     'proof': data.proof,
#     'encryption': data.encryption
#     }
#
#
# def dict2BlockS(d):
#     return BlockS(d['index'], d['timestamp'],d['doctor'], d['patient'],d['describe'],d['proof'], d['encryption'])
#
#
# if __name__ == "__main__":
#     s = BlockS("132", "2","3","3","34","43","32")
#     json_str = json.dumps(s, default=BlockS2dict)
#     print(json_str)
#     d_format = json.loads(json_str, object_hook=dict2BlockS)
#     print(d_format.timestamp)