from flask_security import Security, SQLAlchemyUserDatastore
from src.user import models

user_data_store = SQLAlchemyUserDatastore(models.db, models.User, models.Role)


class FlaskSecurityAdmin(Security):

    def __init__(self,  **kwargs):
        super(FlaskSecurityAdmin, self).__init__(datastore=user_data_store, **kwargs)

    def init_app(self, app, datastore=None, register_blueprint=True,
                 login_form=None, confirm_register_form=None,
                 register_form=None, forgot_password_form=None,
                 reset_password_form=None, change_password_form=None,
                 send_confirmation_form=None, passwordless_login_form=None,
                 anonymous_user=None):
        pass

security = FlaskSecurityAdmin()
