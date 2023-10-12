import traceback
from sqlalchemy import text, or_
from database.database import db
from src.models.Comment import Comment
from src.models.Like import Like
from src.models.Post import Post
from src.share.Result import Result
from sqlalchemy import func
from flask import current_app


def get_all(page, per_page):
    """Get all posts"""
    try:
        posts = Post.query.all() \
            if page == -1 \
            else Post.query.paginate(page=page, per_page=per_page)
        current_app.logger.info("Get all posts")
        return Result.success(posts)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception in get_all: {}".format(str(e)))
        return Result.failed("Error: post_repo " + str(e))


def get_by_id(post_id):
    """Get a post by id"""
    try:
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            current_app.logger.error("Post doesn't exist: {}".format(str(post_id)))
            return Result.failed("Post doesn't exist: " + str(post_id))
        current_app.logger.info("Get a post by id")
        return Result.success(post)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception in get_by_id: {}".format(str(e)))
        return Result.failed("Error: post_repo " + str(e))


def save(data, author_id):
    """Create new post"""
    try:
        db.session.begin()
        new_post = Post(data['title'], data['short_description'], data['body'], author_id)
        db.session.add(new_post)
        db.session.commit()
        db.session.flush()
        db.session.refresh(new_post)
        current_app.logger.info("Create new post")
        return Result.success(new_post)
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        current_app.logger.exception("Exception in save: {}".format(str(e)))
        return Result.failed("Cannot save" + str(e))


def update(old_post, post, author_id):
    """Update a post"""
    try:
        db.session.begin()
        if post['title']:
            old_post.title = post['title']
        if post['short_description']:
            old_post.short_description = post['short_description']
        if post['body']:
            old_post.body = post['body']
        old_post.author_id = int(author_id)
        db.session.commit()
        db.session.flush()
        db.session.refresh(old_post)
        current_app.logger.info("Update a post")
        return Result.success(old_post)
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        current_app.logger.exception("Exception in update: {}".format(str(e)))
        return Result.failed("Cannot save" + str(e))


def delete(post):
    """Delete a post"""
    try:
        db.session.begin()
        db.session.delete(post)
        db.session.commit()
        current_app.logger.info("Delete a post")
        return Result.success(post)
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        current_app.logger.exception("Exception in delete: {}".format(str(e)))
        return Result.failed("Cannot save" + str(e))


def sort_posts(sort_by, page, per_page):
    """Sort posts"""
    try:
        posts = Post.query.outerjoin(Comment, Post.id == Comment.post_id) \
            .outerjoin(Like, Post.id == Like.post_id) \
            .order_by(text(sort_by)).group_by(Post.id).all() \
            if page == -1 \
            else Post.query.outerjoin(Comment, Post.id == Comment.post_id) \
            .outerjoin(Like, Post.id == Like.post_id) \
            .order_by(text(sort_by)).group_by(Post.id) \
            .paginate(page=page, per_page=per_page)
        current_app.logger.info("Sort posts")
        return Result.success(posts)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception in sort_posts: {}".format(str(e)))
        return Result.failed("Error: post_repo " + str(e))


def search_post(keyword):
    """Search Post"""
    try:
        posts = Post.query.outerjoin(Comment, Post.id == Comment.post_id) \
            .outerjoin(Like, Post.id == Like.post_id) \
            .filter(or_(Post.title.like(keyword), Post.short_description.like(keyword))) \
            .order_by(func.count(Like.id).desc(), func.count(Comment.id).desc(), Post.created_at.desc()) \
            .group_by(Post.id).limit(5)
        current_app.logger.info("Search posts")
        return Result.success(posts)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception in search_post: {}".format(str(e)))
        return Result.failed("Error: post_repo " + str(e))
