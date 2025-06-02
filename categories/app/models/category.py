from app.extensions import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Category(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}
