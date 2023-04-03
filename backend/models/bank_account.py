from db import db


class BankAccountModel(db.Model):
    __tablename__ = "bank_accounts"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float(precision=2), unique=False, nullable=False)
    customers = db.relationship(
        "CustomerModel",
        back_populates="bank_accounts",
        secondary="bank_accounts_customers",
    )
