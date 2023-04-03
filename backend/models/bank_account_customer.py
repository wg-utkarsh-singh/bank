from db import db


class BankAccountCustomer(db.Model):
    __tablename__ = "bank_accounts_customers"
    id = db.Column(db.Integer, primary_key=True)
    bank_account_id = db.Column(db.Integer, db.ForeignKey("bank_accounts.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
