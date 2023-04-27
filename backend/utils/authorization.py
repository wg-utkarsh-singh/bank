from flask_jwt_extended import get_jwt, jwt_required


@jwt_required()
def role_in(roles):
    claim = get_jwt()
    role = claim["role"]
    return role in roles


@jwt_required()
def is_same_customer(customer_id):
    if not role_in(["customer"]):
        return False

    claim = get_jwt()
    jwt_id = claim["sub"]
    return jwt_id == customer_id


@jwt_required()
def is_linked_customer(bank_account):
    if not role_in(["customer"]):
        return False

    claim = get_jwt()
    jwt_id = claim["sub"]
    customers = bank_account.customers
    customer_ids = map(lambda x: x.id, customers)
    return jwt_id in customer_ids
