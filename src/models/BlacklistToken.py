from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped
from database.database import db


class BlacklistToken(db.Model):
    """
    List stores blacklisted token
    """
    __tablename__ = 'blacklist_tokens'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(db.String(500), unique=True, nullable=False)
    blacklisted_on = mapped_column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "token": self.token,
                "blacklisted_on": self.blacklisted_on.strftime("%m/%d/%Y, %H:%M:%S")
            }
        )

    @staticmethod
    def map_to_object(self):
        return {
                "id": self.id,
                "token": self.token,
                "blacklisted_on": self.blacklisted_on.strftime("%m/%d/%Y, %H:%M:%S")
            }
