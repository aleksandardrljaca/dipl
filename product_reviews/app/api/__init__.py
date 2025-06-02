from app.api.routes import review_bp


def register_blueprint(app):
    app.register_blueprint(review_bp)
