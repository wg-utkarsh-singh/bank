from db import db
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from models import BankAccountModel, TransactionModel
from resources.bank_account import is_linked_customer
from resources.schemas import TransactionSchema

blp = Blueprint("Transaction", "transactions", description="Operations on transactions")


@blp.route("/transactions/<int:bank_account_id>")
class Transaction(MethodView):
    @jwt_required()
    @blp.response(200, TransactionSchema(many=True))
    def get(self, bank_account_id):
        claim = get_jwt()
        role = claim["role"]
        if role not in ["manager", "cashier", "customer"]:
            abort(401, "Unauthorized")

        jwt_id = claim["sub"]
        bank_account = BankAccountModel.query.get_or_404(bank_account_id)
        if role == "customer" and not is_linked_customer(bank_account, jwt_id):
            abort(401, "Unauthorized")

        return TransactionModel.query.filter_by(bank_account_id=bank_account_id)


@blp.route("/transactions")
class TransactionList(MethodView):
    @jwt_required()
    @blp.response(200, TransactionSchema(many=True))
    def get(self):
        claim = get_jwt()
        if claim["role"] not in ["manager", "cashier"]:
            abort(401, "Unauthorized")

        return TransactionModel.query.all()
