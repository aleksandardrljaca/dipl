from sqlalchemy.types import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
        }
