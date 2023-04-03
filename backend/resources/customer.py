from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import CustomerModel
from resources.schemas import CustomerSchema

blp = Blueprint("Customer", "customers", description="Operations on customers")


@blp.route("/customers")
class CustomerList(MethodView):
    @blp.response(200, CustomerSchema(many=True))
    def get(self):
        return CustomerModel.query.all()


@blp.route("/customers/<int:customer_id>")
class Customer(MethodView):
    @blp.response(200, CustomerSchema)
    def get(self, customer_id):
        customer = CustomerModel.query.get_or_404(customer_id)
        return customer

    def delete(self, customer_id):
        store = CustomerModel.query.get_or_404(customer_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Customer deleted"}, 200
