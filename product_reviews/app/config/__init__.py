from app.extensions import db
from app.config.config import Config


def config_app(app):
    app.config.from_object(Config)
    db.init_app(app)
