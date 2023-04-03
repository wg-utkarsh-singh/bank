from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

import models
from db import db
from resources.schemas import (
    AmountSchema,
    BankAccountAndCustomerSchema,
    BankAccountSchema,
)

blp = Blueprint(
    "Bank account", "bankAccounts", description="Operations on bankAccounts"
)
START_BANK_ACCOUNT_ID = 10_00_00_000
MIN_BALANCE = 100


def next_bank_account_id():
    last = models.LastBankAccountIdModel.query.first()
    if not last:
        last = models.LastBankAccountIdModel(id=START_BANK_ACCOUNT_ID)
        db.session.add(last)
    else:
        last.id += 1

    db.session.commit()
    return last.id


@blp.route("/bankAccounts/<int:bank_account_id>")
class BankAccount(MethodView):
    @blp.response(200, BankAccountSchema)
    def get(self, bank_account_id):
        bank_account = models.BankAccountModel.query.get_or_404(bank_account_id)
        return bank_account


@blp.route("/bankAccounts/<int:bank_account_id>/deposit")
class Deposit(MethodView):
    @blp.arguments(AmountSchema)
    @blp.response(200, BankAccountSchema)
    def post(self, amount_data, bank_account_id):
        bank_account = models.BankAccountModel.query.get_or_404(bank_account_id)
        amount = amount_data["amount"]
        bank_account.balance += amount
        transaction = models.TransactionModel(
            bank_account_id=bank_account_id, amount=amount, balance=bank_account.balance
        )
        try:
            db.session.add(bank_account)
            db.session.add(transaction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while depositing money.")

        return bank_account, 201


@blp.route("/bankAccounts/<int:bank_account_id>/withdraw")
class Withdraw(MethodView):
    @blp.arguments(AmountSchema)
    @blp.response(200, BankAccountSchema)
    def post(self, amount_data, bank_account_id):
        bank_account = models.BankAccountModel.query.get_or_404(bank_account_id)
        amount = amount_data["amount"]
        if bank_account.balance - amount < MIN_BALANCE:
            abort(
                400,
                message=f"Minimum balance must be {MIN_BALANCE}.",
            )

        bank_account.balance -= amount
        transaction = models.TransactionModel(
            bank_account_id=bank_account_id,
            amount=-amount,
            balance=bank_account.balance,
        )
        try:
            db.session.add(bank_account)
            db.session.add(transaction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred withdrawing money.")

        return bank_account, 201


@blp.route("/bankAccounts")
class BankAccountList(MethodView):
    @blp.response(200, BankAccountSchema(many=True))
    def get(self):
        return models.BankAccountModel.query.all()

    @blp.arguments(BankAccountSchema)
    @blp.response(201, BankAccountSchema)
    def post(self, bank_acc_data):
        balance = bank_acc_data["balance"]
        if balance < MIN_BALANCE:
            abort(
                400,
                message=f"Minimum balance must be {MIN_BALANCE}.",
            )

        bank_account = models.BankAccountModel(
            id=next_bank_account_id(), balance=balance
        )
        transaction = models.TransactionModel(
            bank_account_id=bank_account.id,
            amount=bank_account.balance,
            balance=bank_account.balance,
        )
        try:
            db.session.add(bank_account)
            db.session.add(transaction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating a bank account.")

        return bank_account, 201


@blp.route("/customers/<int:customer_id>/bankAccounts/<int:bank_account_id>")
class LinkBankAccountToCustomer(MethodView):
    @blp.response(201, BankAccountSchema)
    def post(self, customer_id, bank_account_id):
        customer = models.CustomerModel.query.get_or_404(
            customer_id, description=f"Customer with id {customer_id} not found."
        )
        bank_account = models.BankAccountModel.query.get_or_404(
            bank_account_id,
            description=f"Bank account with id {bank_account_id} not found.",
        )

        customer.bank_accounts.append(bank_account)
        try:
            db.session.add(customer)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while linking bank account.")

        return bank_account, 201

    @blp.response(200, BankAccountAndCustomerSchema)
    def delete(self, customer_id, bank_account_id):
        customer = models.CustomerModel.query.get_or_404(
            customer_id, description=f"Customer with id {customer_id} not found."
        )
        bank_account = models.BankAccountModel.query.get_or_404(
            bank_account_id,
            description=f"Bank account with id {bank_account_id} not found.",
        )

        customer.bank_accounts.remove(bank_account)
        try:
            db.session.add(customer)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while de-linking bank account.")

        return {
            "message": "Bank account de-linked from customer",
            "customer": customer,
            "bank_account": bank_account,
        }, 200
