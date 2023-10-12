import traceback

from database.database import db
from src.models.Comment import Comment
from src.models.User import User
from src.share.Result import Result


def save(post_id, author_id, comment):
    try:
        new_comment = Comment(comment['content'], post_id, author_id)
        db.session.add(new_comment)
        db.session.commit()
        db.session.flush()
        db.session.refresh(new_comment)
        return Result.success(new_comment)
    except Exception as e:
        traceback.print_exc()
        return Result.failed("Cannot save" + str(e))


def get_by_id(comment_id):
    try:
        comment = Comment.query.filter_by(id=comment_id).first()
        return Result.success(comment)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_all_by_post_id(post_id):
    try:
        comments = Comment.query.filter_by(post_id=post_id)
        return Result.success(list(comments))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_all_by_author_id(author_id):
    try:
        comments = Comment.query.filter_by(author_id=author_id)
        return Result.success(list(comments))
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def get_all():
    try:
        comments = Comment.query.all()
        comments = Comment.query.join(User).filter(comments.author_id == User.id).all()
        return comments
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def search_comment(keyword):
    try:
        comments = Comment.query.filter(Comment.content.like(keyword))\
            .order_by(Comment.created_at.desc()) \
            .limit(5)
        return Result.success(comments)
    except Exception as e:
        traceback.print_exc()
        return Result.failed("Error: post_repo " + str(e))
