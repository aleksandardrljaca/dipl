from app.api.routes import users_bp


def register_blueprint(app):
    app.register_blueprint(users_bp)
