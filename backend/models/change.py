from enum import Enum

from sqlalchemy import JSON

from db import db


class ChangeStatus(Enum):
    pending = 1
    accepted = 2
    rejected = 3


class ChangeModel(db.Model):
    __tablename__ = "changes"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(ChangeStatus, create_constraint=True), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    change = db.Column(JSON, nullable=False)
    comment = db.Column(db.String(), unique=False, nullable=True)
