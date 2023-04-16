from hashlib import sha256

from blocklist import BLOCKLIST
from db import db
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from models import CustomerModel, EmployeeModel, LastAccountIdModel, PersonRole
from resources.schemas import LoginSchema, PersonSchema

blp = Blueprint("Person", "persons", description="Operations on persons")
START_ACCOUNT_ID = 10_00_00_000


def hash_password(password):
    return sha256(password.encode("utf-8")).hexdigest()


def next_account_id():
    last = LastAccountIdModel.query.first()
    if not last:
        last = LastAccountIdModel(id=START_ACCOUNT_ID)
        db.session.add(last)
    else:
        last.id += 1

    db.session.commit()
    return last.id


@blp.route("/register")
class PersonRegister(MethodView):
    @blp.arguments(PersonSchema)
    @blp.response(201, PersonSchema)
    def post(self, person_data):
        if (
            person_data["role"] == PersonRole.customer
            and CustomerModel.query.filter(
                CustomerModel.email == person_data["email"]
            ).first()
        ):
            abort(409, message=f"{person_data['email']} already exist in database.")

        if (
            person_data["role"] != PersonRole.customer
            and EmployeeModel.query.filter(
                EmployeeModel.email == person_data["email"]
            ).first()
        ):
            abort(409, message=f"{person_data['email']} already exist in database.")

        if person_data["role"] == PersonRole.customer:
            person = CustomerModel(
                id=next_account_id(),
                email=person_data["email"],
                name=person_data["name"],
                age=person_data["age"],
                gender=person_data["gender"],
                password=hash_password(person_data["password"]),
            )
        else:
            person = EmployeeModel(
                id=next_account_id(),
                role=person_data["role"],
                email=person_data["email"],
                name=person_data["name"],
                age=person_data["age"],
                gender=person_data["gender"],
                password=hash_password(person_data["password"]),
            )

        db.session.add(person)
        db.session.commit()

        return person, 201


@blp.route("/login")
class PersonLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
        if login_data["role"] == PersonRole.customer:
            person = CustomerModel.query.filter_by(id=login_data["id"]).one_or_none()
        else:
            person = EmployeeModel.query.filter_by(id=login_data["id"]).one_or_none()

        if not person or hash_password(login_data["password"]) != person.password:
            abort(401, message="Invalid credentials.")

        access_token = create_access_token(
            identity=person.id, additional_claims={"role": str(login_data["role"])}
        )
        return {"access": access_token}


@blp.route("/logout")
class PersonLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
