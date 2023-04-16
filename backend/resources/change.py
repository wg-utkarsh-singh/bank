from db import db
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from models import ChangeModel, ChangeStatus, CustomerModel
from resources.schemas import ChangeSchema, CommentSchema, PlainChangeSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Change", "changes", description="Operations on changes")


@blp.route("/changes")
class ChangeList(MethodView):
    @blp.response(200, ChangeSchema(many=True))
    def get(self):
        return ChangeModel.query.all()


@blp.route("/customers/<int:customer_id>/requestChange")
class RequestChange(MethodView):
    @jwt_required()
    @blp.arguments(PlainChangeSchema)
    @blp.response(201, ChangeSchema)
    def post(self, change_data, customer_id):
        claim = get_jwt()
        if claim["role"] != "customer" or claim["sub"] != customer_id:
            abort(401, "Unauthorized")

        if change_data["old"].keys() != change_data["new"].keys():
            abort(400, message="Old and new request should contain same keys.")

        customer = CustomerModel.query.get_or_404(customer_id)
        for attribute in change_data["old"]:
            if getattr(customer, attribute) != change_data["old"][attribute]:
                abort(400, message=f"Database mismatch for {attribute!r} attribute.")

        change = ChangeModel(
            status=ChangeStatus.pending,
            customer_id=customer.id,
            change=change_data,
        )

        try:
            db.session.add(change)
            db.session.commit()
        except:
            abort(500, message="An error occurred requesting a change.")

        return change, 201


@blp.route("/changes/<int:change_id>/accept")
class AcceptChange(MethodView):
    @jwt_required()
    @blp.response(200, ChangeSchema)
    def post(self, change_id):
        claim = get_jwt()
        if claim["role"] != "manager":
            abort(401, "Unauthorized")

        change = ChangeModel.query.get_or_404(change_id)
        if change.status != ChangeStatus.pending:
            abort(409, message="Change not in an pending state.")

        customer = CustomerModel.query.get(change.customer_id)
        new_change = change.change["new"]

        for attribute, value in new_change.items():
            setattr(customer, attribute, value)

        change.status = ChangeStatus.accepted

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred accepting a change request.")

        return change, 200


@blp.route("/changes/<int:change_id>/reject")
class RejectChange(MethodView):
    @jwt_required()
    @blp.arguments(CommentSchema)
    @blp.response(200, ChangeSchema)
    def post(self, comment_data, change_id):
        claim = get_jwt()
        if claim["role"] != "manager":
            abort(401, "Unauthorized")

        change = ChangeModel.query.get_or_404(change_id)
        if change.status != ChangeStatus.pending:
            abort(409, message="Change not in an pending state.")

        change.comment = comment_data["comment"]
        change.status = ChangeStatus.rejected

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred accepting a change request.")

        return change, 200
