from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import EmployeeModel, PersonRole
from resources.schemas import PlainPersonSchema

blp = Blueprint("Cashier", "cashiers", description="Operations on cashiers")


@blp.route("/cashiers")
class CashierList(MethodView):
    @blp.response(200, PlainPersonSchema(many=True))
    def get(self):
        return EmployeeModel.query.filter(
            EmployeeModel.role == PersonRole.cashier
        ).all()


@blp.route("/cashiers/<int:cashier_id>")
class Cashier(MethodView):
    @blp.response(200, PlainPersonSchema)
    def get(self, cashier_id):
        cashier = EmployeeModel.query.filter_by(
            id=cashier_id, role=PersonRole.cashier
        ).first_or_404()
        return cashier

    def delete(self, cashier_id):
        cashier = EmployeeModel.query.filter_by(
            id=cashier_id, role=PersonRole.cashier
        ).first_or_404()
        db.session.delete(cashier)
        db.session.commit()
        return {"message": "Cashier deleted"}, 200
