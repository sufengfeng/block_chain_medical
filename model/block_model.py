# config=utf-8

import sys
import json
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI
from common import db

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)  # echo用于显示sql执行信息,设置SQLAlchemy


class Block(db.Model):
    __tablename__ = 'tb_block'
    index = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)  # 时间戳

    doctor = db.Column(db.String(200), nullable=False)  # 区块拥有者
    patient = db.Column(db.String(200), nullable=False)  # 区块描述对象
    describe = db.Column(db.String(200), nullable=False)  # 描述

    proof = db.Column(db.String(200), nullable=False)  # 证明 无
    encryption = db.Column(db.String(200), nullable=False)  # 同态加密

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

    # 服务器端添加区块，不进行hash识别，只进行hask确认
    @staticmethod
    def server_add_block(block, last_block):
        if block.encryption != hash(last_block):  # 如果本次加入的hash值是上一个区块的hash则认为正确
            print("该区块不满足hash，不能加入到区块链")
            return -1
        Session_class = sessionmaker(bind=engine)  # 建立与数据库的会话连接，这里建立的是一个class不是一个实例对象
        session = Session_class()  # 这里创建一个会话实例
        try:
            session.add(block)  # 把要创建的数据对象加入到这个会话中，这个时候是pending状态，添加多个对象使用add_all()
            session.commit()  # 统一提交会话中的操作
            session.close()
            return 0
        except Exception as e:
            print(str(sys._getframe().f_lineno))
            print(e)
            return -1

    # 添加区块,使用该函数表示block已经计算完毕，等待确认后直接加入到区块链
    @staticmethod
    def add_block(block, last_block):
        if block.encryption != hash(last_block):  # 如果本次加入的hash值是上一个区块的hash则认为正确
            print("该区块不满足hash，不能加入到区块链")
            return -1
        Session_class = sessionmaker(bind=engine)  # 建立与数据库的会话连接，这里建立的是一个class不是一个实例对象
        session = Session_class()  # 这里创建一个会话实例
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
    def blocks_clean():
        Session_class = sessionmaker(bind=engine)  # 建立与数据库的会话连接，这里建立的是一个class不是一个实例对象
        session = Session_class()  # 这里创建一个会话实例
        try:
            session.query(Block).filter().delete()
            session.commit()

            session.close()
            # session.flush()  # 再flush
        except Exception as e:
            print(str(sys._getframe().f_lineno))
            print(e)
            session.rollback()

    @staticmethod
    def Block2dict(data):
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
    def dict2Block(d):
        return Block(d['index'], d['timestamp'], d['doctor'], d['patient'], d['describe'], d['proof'], d['encryption'])


db.Model.metadata.create_all(engine)  # 通过基类与数据库进行交互创建表结构，此时表内还没有数据

if __name__ == "__main__":
    s = Block("132", "2", "3", "3", "34", "43", "32")
    json_str = json.dumps(s, default=Block.Block2dict)
    print(json_str)
    d_format = json.loads(json_str, object_hook=Block.dict2Block)
    print(d_format.timestamp)
