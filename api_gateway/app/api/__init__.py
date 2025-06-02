from app.api.routes import gateway_bp


def register_blueprint(app):
    app.register_blueprint(gateway_bp)
