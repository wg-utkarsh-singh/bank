import resources.schemas as schemas
from db_handlers import bank_account_db, customer_db
from flask import current_app as app
from utils import arguments, response
from utils.authorization import is_linked_customer, role_in

MIN_BALANCE = 100


@app.route("/bankAccounts")
@response(200, schemas.BankAccountSchema(many=True))
def get_bank_accounts():
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    bank_accounts = bank_account_db.get()
    return bank_accounts, 200


@app.route("/bankAccounts/<int:bank_account_id>")
@response(200, schemas.BankAccountSchema)
def get(bank_account_id):
    if not role_in(["manager", "cashier"]) and not is_linked_customer(bank_account):
        return {"message": "Unauthorized"}, 401

    bank_account = bank_account_db.get(bank_account_id)
    if not bank_account:
        return {"message": "Bank account not found"}, 404

    return bank_account, 200


@app.route("/bankAccounts", methods=["POST"])
@arguments(schemas.BankAccountSchema)
@response(201, schemas.BankAccountSchema)
def post_bank_account(bank_acc_data):
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    balance = bank_acc_data["balance"]
    if balance < MIN_BALANCE:
        return {"message": f"Minimum balance must be {MIN_BALANCE}."}, 400

    bank_account = bank_account_db.post(balance)
    if not bank_account:
        return {"message": "An error occurred while posting a bank account"}, 500

    return bank_account, 201


@app.route("/bankAccounts/<int:bank_account_id>/deposit", methods=["POST"])
@arguments(schemas.AmountSchema)
@response(201, schemas.BankAccountSchema)
def deposit(amount_data, bank_account_id):
    bank_account = bank_account_db.get(bank_account_id)
    if not bank_account:
        return {"message": "Bank account not found"}, 404

    if not role_in(["manager", "cashier"]) and not is_linked_customer(bank_account):
        return {"message": "Unauthorized"}, 401

    amount = amount_data["amount"]
    bank_account = bank_account_db.deposit(bank_account, amount)
    if not bank_account:
        return {"message": "An error occurred while depositing to bank account"}, 500

    return bank_account, 201


@app.route("/bankAccounts/<int:bank_account_id>/withdraw", methods=["POST"])
@arguments(schemas.AmountSchema)
@response(201, schemas.BankAccountSchema)
def withdraw(amount_data, bank_account_id):
    bank_account = bank_account_db.get(bank_account_id)
    if not bank_account:
        return {"message": "Bank account not found"}, 404

    if not role_in(["manager", "cashier"]) and not is_linked_customer(bank_account):
        return {"message": "Unauthorized"}, 401

    amount = amount_data["amount"]
    bank_account = bank_account_db.withdraw(bank_account, amount)
    if not bank_account:
        return {"message": "An error occurred while withdrawing from bank account"}, 500

    return bank_account, 201


@app.route(
    "/customers/<int:customer_id>/bankAccounts/<int:bank_account_id>",
    methods=["POST"],
)
@response(201, schemas.BankAccountSchema)
def link_bank_account_to_customer(customer_id, bank_account_id):
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    customer = customer_db.get(customer_id)
    if not customer:
        return {"message": "Customer not found"}, 404

    bank_account = bank_account_db.get(bank_account_id)
    if not bank_account:
        return {"message": "Bank account not found"}, 404

    bank_account = bank_account_db.link(bank_account, customer)
    if not bank_account:
        return {
            "message": "An error occurred while linking bank account to customer"
        }, 500

    return bank_account, 201


@app.route(
    "/customers/<int:customer_id>/bankAccounts/<int:bank_account_id>",
    methods=["DELETE"],
)
@response(200, schemas.BankAccountAndCustomerSchema)
def delink_bank_account_to_customer(customer_id, bank_account_id):
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    customer = customer_db.get(customer_id)
    if not customer:
        return {"message": "Customer not found"}, 404

    bank_account = bank_account_db.get(bank_account_id)
    if not bank_account:
        return {"message": "Bank account not found"}, 404

    bank_account = bank_account_db.delink(bank_account, customer)
    if not bank_account:
        return {
            "message": "An error occurred while de-linking bank account to customer"
        }, 500

    return bank_account, 201
