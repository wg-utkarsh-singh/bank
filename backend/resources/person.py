from blocklist import BLOCKLIST
from db_handlers import cashier_db, customer_db, manager_db
from flask import current_app as app
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from resources.schemas import LoginSchema, PersonSchema
from utils import arguments, hash_password, response


@app.route("/register", methods=["POST"])
@arguments(PersonSchema)
@response(201, PersonSchema)
def register(person_data):
    for db in [customer_db, manager_db, cashier_db]:
        if db.is_registered(person_data["role"], person_data["email"]):
            return {
                "message": f"{person_data['email']} already exist in database."
            }, 409

    person = None
    for db in [customer_db, manager_db, cashier_db]:
        if person := db.post(**person_data):
            break

    return person, 201


@app.route("/login", methods=["POST"])
@arguments(LoginSchema)
def login(login_data):
    for db in [customer_db, manager_db, cashier_db]:
        if person := db.is_registered(login_data["role"], login_data["email"]):
            break

    if not person or hash_password(login_data["password"]) != person.password:
        return {"message": "Invalid credentials."}, 401

    access_token = create_access_token(
        identity=person.id, additional_claims={"role": str(login_data["role"])}
    )
    return {"access": access_token}


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return {"message": "Successfully logged out"}, 200
