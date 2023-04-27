import db
from db_handlers import account_db
from models import EmployeeModel, PersonRole
from utils import hash_password


def is_registered(role, email):
    return (
        role == PersonRole.manager
        and EmployeeModel.query.filter(EmployeeModel.email == email).first()
    )


def get(id=None):
    if id:
        manager = EmployeeModel.query.filter_by(id=id, role=PersonRole.manager).first()
        return manager
    else:
        managers = EmployeeModel.query.filter(
            EmployeeModel.role == PersonRole.manager
        ).all()
        return managers


def post(role, email, name, age, gender, password):
    if role != PersonRole.manager:
        return None

    manager = EmployeeModel(
        id=account_db.next(),
        role=role,
        email=email,
        name=name,
        age=age,
        gender=gender,
        password=hash_password(password),
    )
    if not db.add(manager):
        return None

    return manager


def delete(manager):
    if not db.delete(manager):
        return False

    return True
