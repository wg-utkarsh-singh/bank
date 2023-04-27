import db
from models import BankAccountModel, LastBankAccountIdModel, TransactionModel

START_BANK_ACCOUNT_ID = 10_00_00_000


def next():
    last = LastBankAccountIdModel.query.first()
    if last:
        last.id += 1
    else:
        last = LastBankAccountIdModel(id=START_BANK_ACCOUNT_ID)

    if not db.add(last):
        return None

    return last.id


def get(id=None):
    if id:
        return BankAccountModel.query.get(id)
    else:
        return BankAccountModel.query.all()


def post(balance):
    id = next()
    if not id:
        return None

    bank_account = BankAccountModel(id=id, balance=balance)
    transaction = TransactionModel(
        bank_account_id=bank_account.id,
        amount=bank_account.balance,
        balance=bank_account.balance,
    )

    if not db.add(bank_account):
        return None
    elif not db.add(transaction):
        return None

    return bank_account


def deposit(bank_account, amount):
    bank_account.balance += amount
    transaction = TransactionModel(
        bank_account_id=bank_account.id, amount=amount, balance=bank_account.balance
    )

    if not db.add(bank_account):
        return None
    elif not db.add(transaction):
        return None

    return bank_account


def withdraw(bank_account, amount):
    bank_account.balance -= amount
    transaction = TransactionModel(
        bank_account_id=bank_account.id,
        amount=-amount,
        balance=bank_account.balance,
    )

    if not db.add(bank_account):
        return None
    elif not db.add(transaction):
        return None

    return bank_account


def link(bank_account, customer):
    customer.bank_accounts.append(bank_account)
    if not db.add(customer):
        return None

    return bank_account


def delink(bank_account, customer):
    customer.bank_accounts.remove(bank_account)
    if not db.add(customer):
        return None

    return bank_account
