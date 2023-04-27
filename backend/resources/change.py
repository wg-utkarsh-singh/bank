import resources.schemas as schemas
from db_handlers import change_db, customer_db
from flask import current_app as app
from utils import arguments, response
from utils.authorization import is_same_customer, role_in


@app.route("/changes")
@response(200, schemas.ChangeSchema(many=True))
def change_list():
    if not role_in(["manager"]):
        return {"message": "Unauthorized"}, 401

    changes = change_db.get()
    return changes, 200


@app.route("/customers/<int:customer_id>/requestChange", methods=["POST"])
@arguments(schemas.PlainChangeSchema)
@response(201, schemas.ChangeSchema)
def request_change(change_data, customer_id):
    if not role_in(["manager"]) and not is_same_customer(customer_id):
        return {"message": "Unauthorized"}, 401

    if change_data["old"].keys() != change_data["new"].keys():
        return {"message": "Old and new request should contain same keys."}, 400

    customer = customer_db.get(customer_id)
    if not customer:
        return {"message": "Customer not found"}, 404

    for attribute in change_data["old"]:
        if getattr(customer, attribute) != change_data["old"][attribute]:
            return {"message": f"Database mismatch for {attribute!r} attribute."}, 400

    change = change_db.post(customer_id, change_data)
    if not change:
        return {"message": "An error occurred requesting a change."}, 500

    return change, 201


@app.route("/changes/<int:change_id>/accept", methods=["POST"])
@response(200, schemas.ChangeSchema)
def accept_change(change_id):
    if not role_in(["manager"]):
        return {"message": "Unauthorized"}, 401

    change = change_db.get(change_id)
    if not change_db.is_pending(change):
        return {"message": "Change not in an pending state."}, 409

    customer_id = change_db.get_customer_id(change)
    customer = customer_db.get(customer_id)
    change = change_db.accept(change, customer)
    if not change:
        return {"message": "An error occurred accepting a change request."}, 500

    return change, 200


@app.route("/changes/<int:change_id>/reject", methods=["POST"])
@arguments(schemas.CommentSchema)
@response(200, schemas.ChangeSchema)
def reject_change(comment_data, change_id):
    if not role_in(["manager"]):
        return {"message": "Unauthorized"}, 401

    change = change_db.get(change_id)
    if not change_db.is_pending(change):
        return {"message": "Change not in an pending state."}, 409

    change = change_db.reject(change, comment_data["comment"])
    if not change:
        return {"message": "An error occurred rejecting a change request."}, 500

    return change, 200
