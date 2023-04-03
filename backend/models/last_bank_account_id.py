from db import db


class LastBankAccountIdModel(db.Model):
    __tablename__ = "last_bank_account_id"
    id = db.Column(db.Integer, primary_key=True)
