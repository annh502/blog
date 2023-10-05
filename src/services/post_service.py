from src.repository import post_repo, user_repo, like_repo
from src.share.Result import Result


def get_all():
    return post_repo.get_all()


def get_post(post_id):
    return post_repo.get_by_id(post_id)


def create_post(post, author_id):
    try:
        author_result = user_repo.get_by_id(author_id)
        if not author_result.is_success():
            return author_result
        if post['title'] is None:
            return Result.failed("Title must not be null.")
        if post['body'] is None:
            return Result.failed("Body must not be null.")
        return post_repo.save(post, author_id)
    except Exception as e:
        return Result.failed("Error at post_service: " + str(e))


def update_post(post, post_id, author_id):
    try:
        old_post = post_repo.get_by_id(post_id)
        if not old_post.is_success():
            return old_post
        return post_repo.update(old_post.data, post, author_id)
    except Exception as e:
        return Result.failed("Error at post_service: " + str(e))


def delete_post(post_id):
    try:
        post = post_repo.get_by_id(post_id)
        if not post.is_success():
            return post
        return post_repo.delete(post.data)
    except Exception as e:
        return Result.failed("Error at post_service: " + str(e))


def count_likes(post_id):
    try:
        return like_repo.count_likes(post_id)
    except Exception as e:
        return Result.failed("Error in post services: " + str(e))


def like_post(author_id, post_id):
    try:
        if not post_repo.get_by_id(post_id):
            return Result.failed("Post doesn't exist: " + post_id)
        if not user_repo.get_by_id(author_id):
            return Result.failed("User doesn't exist: " + author_id)
        post_like_result = like_repo.get_id_by_post_author(post_id, author_id)
        if post_like_result.is_success():
            return like_repo.delete(post_like_result.data)
        else:
            return like_repo.save(post_id, author_id)
    except Exception as e:
        return Result.failed("Cannot save" + str(e))
