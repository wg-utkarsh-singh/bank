from os import getenv

from blocklist import BLOCKLIST
from db import db
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from routes import register_routes


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Banks REST API"
    app.config["API_VERSION"] = "v1"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "251548810214037062405875964630167068687"

    jwt = JWTManager(app)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    db.init_app(app)

    with app.app_context():
        register_routes(app)

    with app.app_context():
        db.create_all()

    return app
