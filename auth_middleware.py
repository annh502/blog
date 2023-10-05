# a decorator applied to wrapper to make it look like wrapped func
from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from src.share.api.ResponseEntityFactory import *
from src.models.User import User
from src.models.BlacklistToken import BlacklistToken
from src.repository import user_repo


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return unauthorized("Authentication Token is missing!")

        try:
            if BlacklistToken.query.filter_by(token=token).first():
                raise jwt.ExpiredSignatureError
            data = User.decode_auth_token(token)
            current_user = user_repo.get_by_id(data)
            if current_user is None:
                return unauthorized("Invalid Authentication token!")
        except jwt.ExpiredSignatureError:
            return unauthorized("Your session is over. Please login again.")
        except jwt.InvalidTokenError:
            return unauthorized("Invalid Auth Token")
        except Exception as e:
            return internal_server_error("Something went wrong: " + str(e))

        return f(token, *args, **kwargs) \
            if f.__name__ == "sign_out" \
            else f(current_user, *args, **kwargs)

    return decorated
