from functools import wraps
from flask_restful import Resource, Api
from flask_security import auth_token_required, roles_required

from .blue_prints import bp

api = Api(bp)


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class BaseResource(Resource):
    method_decorators = [auth_token_required, roles_required('admin')]
