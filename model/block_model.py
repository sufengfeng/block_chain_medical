# config=utf-8
import json

from numpy import unicode

from common import db
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

class Block(db.Model):
    __tablename__ = 'tb_block'
    index = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)           #时间戳

    doctor = db.Column(db.String(200), nullable=False)              #区块拥有者
    patient = db.Column(db.String(200), nullable=False)             #区块描述对象
    describe = db.Column(db.String(200), nullable=False)            #描述

    proof = db.Column(db.String(200), nullable=False)               #证明 无
    encryption = db.Column(db.String(200), nullable=False)       #同态加密

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


def dict2Block(d):
    return Block(d['index'], d['timestamp'],d['doctor'], d['patient'],d['describe'],d['proof'], d['encryption'])


if __name__ == "__main__":
    s = Block("132", "2","3","3","34","43","32")
    json_str = json.dumps(s, default=Block2dict)
    print(json_str)
    d_format = json.loads(json_str, object_hook=dict2Block)
    print(d_format.timestamp)
