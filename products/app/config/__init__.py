from app.config.config import Config
from app.extensions import db
from app.extensions import jwt


def config_app(app):
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
