from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ChangeModel, ChangeStatus, CustomerModel
from resources.schemas import ChangeSchema, CommentSchema, PlainChangeSchema

blp = Blueprint("Change", "changes", description="Operations on changes")


@blp.route("/changes")
class ChangeList(MethodView):
    @blp.response(200, ChangeSchema(many=True))
    def get(self):
        return ChangeModel.query.all()


@blp.route("/customers/<int:customer_id>/requestChange")
class RequestChange(MethodView):
    @blp.arguments(PlainChangeSchema)
    @blp.response(201, ChangeSchema)
    def post(self, change_data, customer_id):
        if change_data["old"].keys() != change_data["new"].keys():
            abort(400, message="Old and new request should contain same keys.")

        customer = CustomerModel.query.get_or_404(customer_id)
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
    @blp.response(200, ChangeSchema)
    def post(self, change_id):
        change = ChangeModel.query.get_or_404(change_id)
        if change.status != ChangeStatus.pending:
            abort(409, message="Change not in an pending state.")

        customer = CustomerModel.query.get(change.customer_id)
        new_change = change.change["new"]

        for attribute, value in new_change.items():
            setattr(customer, f"{attribute}", value)

        change.status = ChangeStatus.accepted

        try:
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred accepting a change request.")

        return change, 200


@blp.route("/changes/<int:change_id>/reject")
class RejectChange(MethodView):
    @blp.arguments(CommentSchema)
    @blp.response(200, ChangeSchema)
    def post(self, comment_data, change_id):
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
