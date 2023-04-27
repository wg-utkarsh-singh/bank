from db_handlers import manager_db
from flask import current_app as app
from resources.schemas import PlainPersonSchema
from utils import response
from utils.authorization import role_in


@app.route("/managers")
@response(200, PlainPersonSchema(many=True))
def get_managers_list():
    if not role_in(["manager"]):
        return {"message": "Unauthorized"}, 401

    managers = manager_db.get()
    return managers, 200


@app.route("/managers/<int:manager_id>")
@response(200, PlainPersonSchema)
def get_manager(manager_id):
    if not role_in(["manager"]):
        return {"message": "Unauthorized"}, 401

    manager = manager_db.get(manager_id)
    if not manager:
        return {"message": "Manager not found"}, 404

    return manager, 200


@app.route("/managers/<int:manager_id>", methods=["DELETE"])
def delete_manager(manager_id):
    if not role_in(["manager"]):
        return {"message": "Unauthorized"}, 401

    manager = manager_db.get(manager_id)
    if not manager:
        return {"message": "manager not found"}, 404

    if not manager_db.delete(manager):
        return {"message": "An error occurred while deleting the customer"}, 500

    return {"message": "Manager deleted"}, 200
