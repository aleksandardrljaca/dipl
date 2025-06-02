from flask_jwt_extended import JWTManager
from app.extensions import jwt
from app.config.config import Config
from app.extensions import db
from datetime import timedelta

services = {
    "products": "https://localhost:8080/",
    "product-reviews": "https://localhost:8081/",
    "orders": "https://localhost:8082/",
    "categories": "https://localhost:8083/",
    "users": "https://localhost:8084/",
}


def config_app(app):
    app.config.from_object(Config)
    jwt.init_app(app)
    db.init_app(app)
