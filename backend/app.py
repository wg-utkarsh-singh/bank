from os import getenv

from flask import Flask
from flask_smorest import Api

import resources
from db import db


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Banks REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)

    api.register_blueprint(resources.PersonBlueprint)
    api.register_blueprint(resources.ManagerBlueprint)
    api.register_blueprint(resources.CashierBlueprint)
    api.register_blueprint(resources.CustomerBlueprint)
    api.register_blueprint(resources.BankAccountBlueprint)
    api.register_blueprint(resources.ChangeBlueprint)
    api.register_blueprint(resources.TransactionBlueprint)

    with app.app_context():
        db.create_all()

    return app
