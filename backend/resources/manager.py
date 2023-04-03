from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import EmployeeModel, PersonRole
from resources.schemas import PlainPersonSchema

blp = Blueprint("Manager", "managers", description="Operations on managers")


@blp.route("/managers")
class ManagerList(MethodView):
    @blp.response(200, PlainPersonSchema(many=True))
    def get(self):
        return EmployeeModel.query.filter(
            EmployeeModel.role == PersonRole.manager
        ).all()


@blp.route("/managers/<int:manager_id>")
class Manager(MethodView):
    @blp.response(200, PlainPersonSchema)
    def get(self, manager_id):
        manager = EmployeeModel.query.filter_by(
            id=manager_id, role=PersonRole.manager
        ).first_or_404()
        return manager

    def delete(self, manager_id):
        manager = EmployeeModel.query.filter_by(
            id=manager_id, role=PersonRole.manager
        ).first_or_404()
        db.session.delete(manager)
        db.session.commit()
        return {"message": "Manager deleted"}, 200
