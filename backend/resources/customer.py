from db import db
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from models import CustomerModel
from resources.schemas import CustomerSchema

blp = Blueprint("Customer", "customers", description="Operations on customers")


@blp.route("/customers")
class CustomerList(MethodView):
    @jwt_required()
    @blp.response(200, CustomerSchema(many=True))
    def get(self):
        claim = get_jwt()
        if claim["role"] not in ["manager", "cashier"]:
            abort(401, "Unauthorized")

        return CustomerModel.query.all()


@blp.route("/customers/<int:customer_id>")
class Customer(MethodView):
    @jwt_required()
    @blp.response(200, CustomerSchema)
    def get(self, customer_id):
        claim = get_jwt()
        if claim["role"] not in ["manager", "cashier"]:
            abort(401, "Unauthorized")

        customer = CustomerModel.query.get_or_404(customer_id)
        return customer

    @jwt_required()
    def delete(self, customer_id):
        claim = get_jwt()
        if claim["role"] not in ["manager", "cashier"]:
            abort(401, "Unauthorized")

        store = CustomerModel.query.get_or_404(customer_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Customer deleted"}, 200
