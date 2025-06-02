from app.api.routes import orders_bp


def register_blueprint(app):
    app.register_blueprint(orders_bp)
