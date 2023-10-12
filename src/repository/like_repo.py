import traceback

from database.database import db
from src.models.Like import Like
from src.share.Result import Result


def save(post_id, author_id):
    try:
        like = Like(post_id, author_id)
        db.session.add(like)
        db.session.commit()
        db.session.flush()
        db.session.refresh(like)

        return Result.success(like)
    except Exception as e:
        traceback.print_exc()
        return Result.failed("Cannot save" + str(e))


def get_id_by_post_author(post_id, author_id):
    try:
        post_like = Like.query.filter_by(post_id=post_id, author_id=author_id).first()
        return Result.success(post_like) \
            if post_like \
            else Result.failed("Cannot found")
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_by_id(like_id):
    try:
        likes = Like.query.filter_by(id=like_id)
        return Result.success(list(likes))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_all_by_post_id(post_id):
    try:
        likes = Like.query.filter_by(post_id=post_id)
        return Result.success(list(likes))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def count_likes(post_id):
    try:
        likes = Like.query.filter_by(post_id=post_id).count()
        return Result.success(likes)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def delete(like_id):
    try:
        like = get_by_id(like_id)
        if isinstance(like, Like):
            db.session.delete(like)
            db.session.commit()
            return Result.success(like.id)
        return like
    except Exception as e:
        return Result.failed("Cannot save" + str(e))
