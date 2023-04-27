from db_handlers import bank_account_db, transaction_db
from flask import current_app as app
from resources.schemas import TransactionSchema
from utils import response
from utils.authorization import is_linked_customer, role_in


@app.route("/transactions")
@response(200, TransactionSchema(many=True))
def get_transaction_list():
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    transactions = transaction_db.get()
    return transactions, 200


@app.route("/transactions/<int:bank_account_id>")
@response(200, TransactionSchema(many=True))
def get_transaction(bank_account_id):
    bank_account = bank_account_db.get(bank_account_id)
    if not bank_account:
        return {"message": "Bank account not found"}, 404

    if not role_in(["manager", "cashier"]) and not is_linked_customer(bank_account):
        return {"message": "Unauthorized"}, 401

    transactions = transaction_db.filter(bank_account_id)
    return transactions, 200
