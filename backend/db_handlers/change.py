import db
from models import ChangeModel, ChangeStatus


def is_pending(change):
    return change.status == ChangeStatus.pending


def get(id=None):
    if id:
        return ChangeModel.query.get(id)
    else:
        return ChangeModel.query.all()


def get_customer_id(change):
    return change.customer_id


def post(customer_id, change):
    change = ChangeModel(
        status=ChangeStatus.pending,
        customer_id=customer_id,
        change=change,
    )
    if not db.add(change):
        return None

    return change


def accept(change, customer):
    new_change = change.change["new"]

    for attribute, value in new_change.items():
        setattr(customer, attribute, value)

    change.status = ChangeStatus.accepted

    if not db.add(change) or not db.add(customer):
        return None

    return change


def reject(change, comment):
    change.comment = comment
    change.status = ChangeStatus.rejected

    if not db.add(change):
        return None

    return change
