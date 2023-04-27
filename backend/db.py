from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


def db_exception_handler(func):
    @wraps(func)
    def wrapper_db_exception_handler(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SQLAlchemyError:
            return False
        else:
            return True

    return wrapper_db_exception_handler


@db_exception_handler
def add(obj):
    db.session.add(obj)
    db.session.commit()


@db_exception_handler
def delete(obj):
    db.session.delete(obj)
    db.session.commit()
