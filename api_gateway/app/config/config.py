from datetime import timedelta


class Config:
    JWT_SECRET_KEY = "put your secret here"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=3)
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://your-user:your-password@localhost:9000/token_blocklist"
    )
