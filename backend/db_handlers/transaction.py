from models import TransactionModel


def get(id=None):
    if id:
        return TransactionModel.query.get(id)
    else:
        return TransactionModel.query.all()


def filter(bank_account_id):
    return TransactionModel.query.filter_by(bank_account_id=bank_account_id)
