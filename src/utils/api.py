from flask_restful import Resource, Api
from functools import wraps
from .blue_prints import bp

api = Api(bp)


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class BaseResource(Resource):
    method_decorators = [authenticate]
