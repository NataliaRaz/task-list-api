from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from ..db import db

class Task(db.Model):
    __tablename__ = "tasks"

    id:           Mapped[int]       = mapped_column(Integer, primary_key=True, autoincrement=True)
    title:        Mapped[str]       = mapped_column(String, nullable=False)
    description:  Mapped[str]       = mapped_column(Text, nullable=False)
    completed_at: Mapped[DateTime]  = mapped_column(DateTime, nullable=True)

    # ← NEW: FK to goals.id
    goal_id:      Mapped[int|None]  = mapped_column(
                           ForeignKey("goals.id"),
                           nullable=True
    )
    goal:         Mapped["Goal"]    = relationship(
                           "Goal",
                           back_populates="tasks"
    )

    @classmethod
    def from_dict(cls, data):
        return cls(
            title        = data["title"],
            description  = data["description"],
            completed_at = data.get("completed_at")
        )

    def to_dict(self):
        return {
            "id":           self.id,
            "title":        self.title,
            "description":  self.description,
            "is_complete":  bool(self.completed_at)
        }