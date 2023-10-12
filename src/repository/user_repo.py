import traceback

from database.database import db
from src.share.Result import Result
from src.models.User import User
from src.models.BlacklistToken import BlacklistToken
from flask import current_app


def get_all():
    """Get all users"""
    try:
        users = User.query.all()
        current_app.logger.info("Get all users")
        return Result.success(users)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception while get all users: {}".format(e))
        return Result.failed(e)


def get_by_id(user_id):
    """Get a user by id"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        current_app.logger.info("User doesn't exist: {}".format(str(user_id)))
        return Result.failed("User doesn't exist: " + str(user_id))
    current_app.logger.info("Get user with id: {}".format(str(user_id)))
    return Result.success(user)


def get_by_email(email):
    """Get a user by email"""
    user = User.query.filter_by(email=email).first()
    if not user:
        current_app.logger.info("User doesn't exist: {}".format(str(email)))
        return Result.failed("User doesn't exist: " + str(email))
    current_app.logger.info("Get user with id: {}".format(str(email)))
    return Result.success(user)


def save(new_user):
    """Create a new user"""
    try:
        db.session.begin()
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info("Add new user success!")
        return Result.success(new_user)
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        current_app.logger.exception("Add new user failed!")
        return Result.failed("Cannot save" + str(e))


def logout(token):
    """Log out an user"""
    try:
        db.session.begin()
        blacklist_token = BlacklistToken(token)
        db.session.add(blacklist_token)
        db.session.commit()
        current_app.logger.info("Log user out success!")
        return Result.success(blacklist_token)
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        current_app.logger.exception("Log user out failed!")
        return Result.failed("Cannot save" + str(e))


def update(old_user, user):
    """Update a user"""
    try:
        db.session.begin()
        if user["name"]:
            old_user.username = user['name']
        if user["email"]:
            old_user.email = user["email"]
        db.session.commit()
        current_app.logger.info("Update user success!")
        return Result.success(old_user)
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        current_app.logger.exception("Update user failed!")
        return Result.failed("Cannot save" + str(e))


def delete(user):
    try:
        db.session.begin()
        db.session.delete(user)
        db.session.commit()
        current_app.logger.info("Delete user success!")
        return Result.success(user)
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        current_app.logger.exception("Delete user failed!")
        return Result.failed("Cannot save" + str(e))
