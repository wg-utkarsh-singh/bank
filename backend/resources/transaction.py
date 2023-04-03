from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import TransactionModel
from resources.schemas import TransactionSchema

blp = Blueprint("Transaction", "transactions", description="Operations on transactions")


@blp.route("/transactions")
class TransactionList(MethodView):
    @blp.response(200, TransactionSchema(many=True))
    def get(self):
        return TransactionModel.query.all()
