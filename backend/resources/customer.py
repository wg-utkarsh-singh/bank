from db_handlers import customer_db
from flask import current_app as app
from resources.schemas import CustomerSchema
from utils import response
from utils.authorization import role_in


@app.route("/customers")
@response(200, CustomerSchema(many=True))
def get_customers():
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    customers = customer_db.get()
    return customers, 200


@app.route("/customers/<int:customer_id>")
@response(200, CustomerSchema)
def get_customer(customer_id):
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    customer = customer_db.get(customer_id)
    if not customer:
        return {"message": "Customer not found"}, 404

    return customer, 200


@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    customer = customer_db.get(customer_id)
    if not customer:
        return {"message": "Customer not found"}, 404

    if not customer_db.delete(customer):
        return {"message": "An error occurred while deleting the customer"}, 500

    return {"message": "Customer deleted"}, 200
