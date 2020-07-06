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

class Record(db.Model):
    __tablename__ = 'tb_record'
    index = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)           #时间戳
    pre_describe = db.Column(db.String(200), nullable=False)
    describe = db.Column(db.String(200), nullable=False)             #区块描述对象

    def __init__(self, index=None, timestamp=None,  pre_describe=None, describe=None):
        self.index = index
        self.timestamp = timestamp
        self.pre_describe=pre_describe
        self.describe = describe

