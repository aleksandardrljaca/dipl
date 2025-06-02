from app.config.config import Config
from app.extensions import db


def config_app(app):
    app.config.from_object(Config)
    db.init_app(app)
