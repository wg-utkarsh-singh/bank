from db import db
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from models import EmployeeModel, PersonRole
from resources.schemas import PlainPersonSchema

blp = Blueprint("Cashier", "cashiers", description="Operations on cashiers")


@blp.route("/cashiers")
class CashierList(MethodView):
    @jwt_required()
    @blp.response(200, PlainPersonSchema(many=True))
    def get(self):
        claim = get_jwt()
        if claim["role"] != "manager":
            abort(401, "Unauthorized")

        return EmployeeModel.query.filter(
            EmployeeModel.role == PersonRole.cashier
        ).all()


@blp.route("/cashiers/<int:cashier_id>")
class Cashier(MethodView):
    @jwt_required()
    @blp.response(200, PlainPersonSchema)
    def get(self, cashier_id):
        claim = get_jwt()
        if claim["role"] != "manager":
            abort(401, "Unauthorized")

        cashier = EmployeeModel.query.filter_by(
            id=cashier_id, role=PersonRole.cashier
        ).first_or_404()
        return cashier

    @jwt_required()
    def delete(self, cashier_id):
        claim = get_jwt()
        if claim["role"] != "manager":
            abort(401, "Unauthorized")

        cashier = EmployeeModel.query.filter_by(
            id=cashier_id, role=PersonRole.cashier
        ).first_or_404()
        db.session.delete(cashier)
        db.session.commit()
        return {"message": "Cashier deleted"}, 200
