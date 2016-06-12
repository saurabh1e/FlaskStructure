from flask import Flask

from .api import api, BaseResource, OpenResource, CommonResource, StudentResource, CounsellorResource
from .models import db, ReprMixin, BaseMixin
from .factory import create_app
from .schema import ma
from .blue_prints import bp
from .admin import admin
from src.config import configs

app = Flask(__name__)

app.config.from_object(configs.get('default'))


