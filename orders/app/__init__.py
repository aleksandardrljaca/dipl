from flask import Flask
from app.config import config_app
from app.api import register_blueprint
from app.extensions import db


def create_app():
    app = Flask(__name__)
    config_app(app)
    register_blueprint(app)
    with app.app_context():
        db.create_all()
    return app
