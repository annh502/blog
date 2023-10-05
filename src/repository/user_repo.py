import traceback

from database.database import db
from src.share.Result import Result
from src.models.User import User
from src.models.BlacklistToken import BlacklistToken
from sqlalchemy import desc, asc


def mapp(list):
    result = []
    for self in list:
        x_object = {
                "id": self.id,
                "email": self.email,
                "username": self.username,
                "registered_on": self.registered_on.strftime("%m/%d/%Y, %H:%M:%S")
            }
        result.append(x_object)
    return result


def get_all():
    """Get all users"""
    """
    SELECT * FROM users
    ORDER BY users.registered_on DESC
    """
    users = User.query.order_by(desc(User.registered_on)).all()
    return users


def get_by_id(user_id):
    """Get a user by id"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return Result.failed("User doesn't exist: " + str(user_id))
    return Result.success(user)


def get_by_email(email):
    """Get a user by email"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return Result.failed(email)
    return Result.success(user)


def save(new_user):
    """Create a new user"""
    try:
        db.session.add(new_user)
        print(new_user.__repr__())
        db.session.commit()
        return Result.success(new_user)
    except Exception as e:
        traceback.print_exc()
        return Result.failed("Cannot save" + str(e))


def logout(token):
    """Log out an user"""
    try:
        blacklist_token = BlacklistToken(token)
        db.session.add(blacklist_token)
        db.session.commit()
        return Result.success(blacklist_token)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def update(old_user, user):
    """Update a user"""
    try:
        if user["name"]:
            old_user.username = user['name']
        if user["email"]:
            old_user.email = user["email"]
        db.session.commit()
        return Result.success(old_user)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def delete(user):
    try:
        db.session.delete(user)
        db.session.commit()
        return Result.success(user)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))
