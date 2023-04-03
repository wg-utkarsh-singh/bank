from db import db


class LastAccountIdModel(db.Model):
    __tablename__ = "last_account_id"
    id = db.Column(db.Integer, primary_key=True)
