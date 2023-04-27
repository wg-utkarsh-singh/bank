import db
from db_handlers import account_db
from models import CustomerModel, PersonRole
from utils import hash_password


def is_registered(role, email):
    return (
        role == PersonRole.customer
        and CustomerModel.query.filter(CustomerModel.email == email).first()
    )


def get(id=None):
    if id:
        customer = CustomerModel.query.get(id)
        return customer
    else:
        customers = CustomerModel.query.all()
        return customers


def post(role, email, name, age, gender, password):
    if role != PersonRole.customer:
        return None

    customer = CustomerModel(
        id=account_db.next(),
        email=email,
        name=name,
        age=age,
        gender=gender,
        password=hash_password(password),
    )
    if not db.add(customer):
        return None

    return customer


def delete(customer):
    if not db.delete(customer):
        return False
    return True
