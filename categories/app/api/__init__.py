from app.api.routes import categories_bp
from flask import Flask


def register_blueprint(app):
    app.register_blueprint(categories_bp)
