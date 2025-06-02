from flask import Flask
from app.extensions import db


def create_app():
    app = Flask(__name__)
    from .config import config_app

    config_app(app)
    from .api import register_blueprint

    register_blueprint(app)
    with app.app_context():
        db.create_all()
    return app
