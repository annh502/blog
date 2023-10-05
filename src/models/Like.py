from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database.database import db


class Like(db.Model):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    created_at = mapped_column(db.DateTime(timezone=True), default=func.now())
    post_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("posts.id", ondelete='CASCADE'), nullable=False)
    author_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

    def __init__(self, post_id, author_id):
        self.post_id = post_id
        self. author_id = author_id

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "post_id": self.post_id,
                "author_id": self.author_id,
                "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            }
        )

    @staticmethod
    def map_to_object(self):
        return {
                "id": self.id,
                "post_id": self.post_id,
                "author_id": self.author_id,
                "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
            }
