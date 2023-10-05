from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database.database import db


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    content = mapped_column(db.String(1000), nullable=False)
    created_at = mapped_column(db.DateTime(timezone=True), default=func.now())
    updated_at = mapped_column(
        db.DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    post_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("posts.id", ondelete='CASCADE'), nullable=False)
    author_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

    def __init__(self, content, post_id, author_id):
        self.content = content
        self.post_id = post_id
        self.author_id = author_id

    def __repr__(self):
        return str(
            {"id": self.id,
             "content": self.content,
             "post_id": self.post_id,
             "author_id": self.author_id,
             "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S") if self.created_at else None,
             "updated_at": self.updated_at.strftime("%m/%d/%Y, %H:%M:%S") if self.updated_at else None
             }
        )

    @staticmethod
    def map_to_object(self):
        return {
             "id": self.id,
             "content": self.content,
             "post_id": self.post_id,
             "author_id": self.author_id,
             "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S") if self.created_at else None,
             "updated_at": self.updated_at.strftime("%m/%d/%Y, %H:%M:%S") if self.updated_at else None
        }
