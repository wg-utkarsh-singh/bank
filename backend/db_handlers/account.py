import db
from models import LastAccountIdModel

START_ACCOUNT_ID = 10_00_00_000


def next():
    last = LastAccountIdModel.query.first()
    if last:
        last.id += 1
    else:
        last = LastAccountIdModel(id=START_ACCOUNT_ID)

    if not db.add(last):
        return None

    return last.id
