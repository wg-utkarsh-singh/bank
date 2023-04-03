from db import db


class TransactionModel(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    bank_account_id = db.Column(db.Integer, db.ForeignKey("bank_accounts.id"))
    amount = db.Column(db.Float(precision=2), unique=False, nullable=False)
    balance = db.Column(db.Float(precision=2), unique=False, nullable=False)
