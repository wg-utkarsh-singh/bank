import db
from db_handlers import account_db
from models import EmployeeModel, PersonRole
from utils import hash_password


def is_registered(role, email):
    return (
        role == PersonRole.cashier
        and EmployeeModel.query.filter(EmployeeModel.email == email).first()
    )


def get(id=None):
    if id:
        cashier = EmployeeModel.query.filter_by(id=id, role=PersonRole.cashier).first()
        return cashier
    else:
        cashiers = EmployeeModel.query.filter(
            EmployeeModel.role == PersonRole.cashier
        ).all()
        return cashiers


def post(role, email, name, age, gender, password):
    if role != PersonRole.cashier:
        return None

    cashier = EmployeeModel(
        id=account_db.next(),
        role=role,
        email=email,
        name=name,
        age=age,
        gender=gender,
        password=hash_password(password),
    )
    if not db.add(cashier):
        return None

    return cashier


def delete(cashier):
    if not db.delete(cashier):
        return False

    return True
