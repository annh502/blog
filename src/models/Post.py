from database.database import db
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column


class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)
    short_description: Mapped[str] = mapped_column(db.String(300))
    body: Mapped[str] = mapped_column(db.Text, nullable=False)
    created_at = mapped_column(db.DateTime(timezone=True), default=func.now())
    author_id: Mapped[int] = mapped_column(db.Integer,
                                           db.ForeignKey("users.id", ondelete="CASCADE"),
                                           nullable=False)

    def __init__(self, title, short_description, body, author_id):
        self.title = title
        self.short_description = short_description
        self.body = body
        self.author_id = author_id

    @staticmethod
    def map_to_object(self):
        return {"id": self.id,
                "title": self.title,
                "short_description": self.short_description,
                "body": self.body,
                "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            }

    def __repr__(self):
        return str(
            {"id": self.id,
                "title": self.title,
                "short_description": self.short_description,
                "body": self.body,
                "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            }
        )
