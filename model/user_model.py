# config=utf-8
from flask_login import UserMixin
from numpy import unicode

from common import db

class User(db.Model, UserMixin):

    user_id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(200))


    __tablename__ = 'tb_user'

    def __init__(self, user_id=None, role=None, password=None, name="anonymous"):

        self.user_id = user_id
        self.role = role
        self.password = password
        self.name = name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<User %r>' % (self.user_id)

