from enum import Enum

from db import db


class PersonRole(Enum):
    customer = 1
    cashier = 2
    manager = 3


class PersonModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(1), unique=False, nullable=False)
    password = db.Column(db.String(), nullable=False)
