from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # RELACIÓN 1 → N
    animals: Mapped[list["Animal"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "animals": [animal.serialize() for animal in self.animals]
        }


class Animal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=False)

    # FK que apunta al user
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # RELACIÓN inversa
    owner: Mapped["User"] = relationship(back_populates="animals")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "user_id": self.user_id
        }
