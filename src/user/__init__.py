from flask_security import SQLAlchemyUserDatastore
from src import security
from . import models
from . import schemas
from . import apiv1

user_data_store = SQLAlchemyUserDatastore(models.db, models.User, models.Role)
security.datastore = user_data_store
