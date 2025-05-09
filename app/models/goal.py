from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from ..db import db

class Goal(db.Model):
    __tablename__ = "goals"

    id: Mapped[int]    = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="goal",
        cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict:
        return {
            "id":    self.id,
            "title": self.title
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"]
        )