# config=utf-8
import json
import hashlib
import sys
import time

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DEBUG = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/blockchain?charset=utf8'
SECRET_KEY = '*\xff\x93\xc8w\x13\x0e@3\xd6\x82\x0f\x84\x18\xe7\xd9\\|\x04e\xb9(\xfd\xc3'
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)  # echo用于显示sql执行信息,设置SQLAlchemy logging
Base = declarative_base()  # 生成orm基类


# 节点服务器区块结构
class BlockS(Base):
    __tablename__ = 'tb_blocks'
    index = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    timestamp = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)  # 时间戳

    doctor = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)  # 区块拥有者
    patient = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)  # 区块描述对象
    describe = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)  # 描述

    proof = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)  # 证明 无
    encryption = sqlalchemy.Column(sqlalchemy.String(200), nullable=False)  # 同态加密

    def __init__(self, index=None, timestamp=None, doctor=None, patient="anonymous", describe=None, proof="proof",
                 encryption="previous_hash"):
        self.index = index
        self.timestamp = timestamp

        self.doctor = doctor
        self.patient = patient
        self.describe = describe

        self.proof = proof
        self.encryption = encryption

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # 添加区块
    @staticmethod
    def add_blockS(block, last_block):
        Session_class = sessionmaker(bind=engine)  # 建立与数据库的会话连接，这里建立的是一个class不是一个实例对象
        session = Session_class()  # 这里创建一个会话实例
        if last_block != None:
            block.encryption = hash(last_block)  # 同态加密
        else:
            block.encryption = hash(block)  # 同态加密
        try:
            session.add(block)  # 把要创建的数据对象加入到这个会话中，这个时候是pending状态，添加多个对象使用add_all()
            session.commit()  # 统一提交会话中的操作
            session.close()
            return 0
        except Exception as e:
            print(str(sys._getframe().f_lineno))
            print(e)
            return -1

    # 清空区块链数据库
    @staticmethod
    def tb_blocks_clean():
        Session_class = sessionmaker(bind=engine)  # 建立与数据库的会话连接，这里建立的是一个class不是一个实例对象
        session = Session_class()  # 这里创建一个会话实例
        try:
            session.query(BlockS).filter().delete()
            session.commit()
            session.close()
            # session.flush()  # 再flush
        except Exception as e:
            print(str(sys._getframe().f_lineno))
            print(e)
            session.rollback()

    # 添加首个区块
    @staticmethod
    def add_first_block():
        timestamp = time.time()
        BlockS.tb_blocks_clean()
        block = BlockS(index=1, timestamp=timestamp, doctor="admin", patient="patient", describe="None")
        BlockS.add_block(block, last_block=None)

    @staticmethod
    def BlockS2dict(data):
        return {
            'index': data.index,
            'timestamp': data.timestamp,

            'doctor': data.doctor,
            'patient': data.patient,
            'describe': data.describe,

            'proof': data.proof,
            'encryption': data.encryption
        }

    @staticmethod
    def dict2BlockS(d):
        return BlockS(d['index'], d['timestamp'], d['doctor'], d['patient'], d['describe'], d['proof'], d['encryption'])


Base.metadata.create_all(engine)  # 通过基类与数据库进行交互创建表结构，此时表内还没有数据

if __name__ == "__main__":
    BlockS.tb_blocks_clean()
    Session_class = sessionmaker(bind=engine)  # 建立与数据库的会话连接，这里建立的是一个class不是一个实例对象
    session = Session_class()  # 这里创建一个会话实例
    test1 = BlockS(index=None, timestamp="None", doctor="None", patient="anonymous", describe="None", proof="proof",
                   encryption="previous_hash")
    session.add(test1)  # 把要创建的数据对象加入到这个会话中，这个时候是pending状态，添加多个对象使用add_all()
    session.commit()  # 统一提交会话中的操作
    session.close()

    s = BlockS("132", "2", "3", "3", "34", "43", "32")
    json_str = json.dumps(s, default=BlockS2dict)
    print(json_str)
    d_format = json.loads(json_str, object_hook=dict2BlockS)
    print(d_format.timestamp)
