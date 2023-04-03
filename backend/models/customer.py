from db import db
from models.person import PersonModel


class CustomerModel(PersonModel):
    __tablename__ = "customers"
    bank_accounts = db.relationship(
        "BankAccountModel",
        back_populates="customers",
        secondary="bank_accounts_customers",
    )
