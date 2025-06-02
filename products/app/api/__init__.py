from app.api.routes import products_bp


def register_blueprint(app):
    app.register_blueprint(products_bp)
