from database.database import db
from src.models.Post import Post
from src.share.Result import Result


def get_all():
    """Get all posts"""
    try:
        posts = Post.query.all()
        return Result.success(posts)
    except Exception as e:
        return Result.failed("Error: post_repo " + str(e))


def get_by_id(post_id):
    """Get a post by id"""
    try:
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return Result.failed("Post doesn't exist: " + str(post_id))
        return Result.success(post)
    except Exception as e:
        return Result.failed("Error: post_repo " + str(e))


def save(data, author_id):
    """Create new post"""
    try:
        new_post = Post(data['title'], data['short_description'], data['body'], author_id)
        db.session.add(new_post)
        db.session.commit()
        db.session.flush()
        db.session.refresh(new_post)
        return Result.success(new_post)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def update(old_post, post, author_id):
    """Update a post"""
    try:
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
        return Result.success(old_post)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))


def delete(post):
    """Delete a post"""
    try:
        db.session.delete(post)
        db.session.commit()
        return Result.success(post)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))
