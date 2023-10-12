import traceback

from flask import current_app

from src.repository import post_repo, user_repo, like_repo
from src.share.Result import Result


def get_all(page, per_page):
    return post_repo.get_all(page, per_page)


def get_post(post_id):
    return post_repo.get_by_id(post_id)


def create_post(post, author_id):
    try:
        author_result = user_repo.get_by_id(author_id)
        if not author_result.is_success():
            return author_result
        if post['title'] is None:
            current_app.logger.error()
            return Result.failed("Title must not be null.")
        if post['body'] is None:
            return Result.failed("Body must not be null.")
        return post_repo.save(post, author_id)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception in create_post: {}".format(str(e)))
        return Result.failed("Error at post_service: " + str(e))


def update_post(post, post_id, author_id):
    try:
        old_post = post_repo.get_by_id(post_id)
        if not old_post.is_success():
            return old_post
        return post_repo.update(old_post.data, post, author_id)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception in update_post: {}".format(str(e)))
        return Result.failed("Error at post_service: " + str(e))


def delete_post(post_id):
    try:
        post = post_repo.get_by_id(post_id)
        if not post.is_success():
            return post
        return post_repo.delete(post.data)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception in delete_post: {}".format(str(e)))
        return Result.failed("Error at post_service: " + str(e))


def count_likes(post_id):
    try:
        return like_repo.count_likes(post_id)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception in count_likes: {}".format(str(e)))
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
        traceback.print_exc()
        current_app.logger.exception("Exception in like_post: {}".format(str(e)))
        return Result.failed("Cannot save" + str(e))


def sort_posts(sort_by_list, page, per_page):
    try:
        sort_text = ''
        for sort_by in sort_by_list:
            if str(sort_by).lower() not in \
                    ['a created_at', 'a like', 'a comment', 'a title',
                     'd created_at', 'd like', 'd comment', 'd title']:
                return Result.failed("Can not sort by: {}".format(sort_by))
            if sort_by[2:] in ['created_at', 'title']:
                if sort_by[0] == 'a':
                    sort_text = sort_text + "Posts.{} {},".format(sort_by[2:], 'asc')
                else:
                    sort_text = sort_text + "Posts.{} {},".format(sort_by[2:], 'desc')
            else:
                if sort_by[0] == 'a' and sort_by[2:] == 'like':
                    sort_text = sort_text + "count(Likes.id) asc,"
                elif sort_by[0] == 'd' and sort_by[2:] == 'like':
                    sort_text = sort_text + "count(Likes.id) desc,"
                if sort_by[0] == 'a' and sort_by[2:] == 'comment':
                    sort_text = sort_text + "count(Comments.id) asc,"
                elif sort_by[0] == 'd' and sort_by[2:] == 'comment':
                    sort_text = sort_text + "count(Comments.id) desc,"
        a = 1 / 0
        return post_repo.sort_posts(sort_text[:-1], page, per_page)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.exception("Exception in sort_posts: {}".format(str(e)))
        return Result.failed("Cannot save" + str(e))


def search_post(keyword):
    return post_repo.search_post("%{}%".format(keyword))
