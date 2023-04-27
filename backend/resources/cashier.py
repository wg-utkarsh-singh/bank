from db_handlers import cashier_db
from flask import current_app as app
from resources.schemas import PlainPersonSchema
from utils import response
from utils.authorization import role_in


@app.route("/cashiers")
@response(200, PlainPersonSchema(many=True))
def get_cashiers_list():
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    cashiers = cashier_db.get()
    return cashiers, 200


@app.route("/cashiers/<int:cashier_id>")
@response(200, PlainPersonSchema(many=True))
def get_cashier(cashier_id):
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    cashier = cashier_db.get(cashier_id)
    if not cashier:
        return {"message": "Cashier not found"}, 404

    return cashier, 200


@app.route("/cashiers/<int:cashier_id>", methods=["DELETE"])
def delete_cashier(cashier_id):
    if not role_in(["manager", "cashier"]):
        return {"message": "Unauthorized"}, 401

    cashier = cashier_db.get(cashier_id)
    if not cashier:
        return {"message": "Cashier not found"}, 404

    if not cashier_db.delete(cashier):
        return {"message": "An error occurred while deleting the customer"}, 500

    return {"message": "Cashier deleted"}, 200
