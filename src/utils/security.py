from flask_security import Security


class FlaskSecurityAdmin(Security):

    def __init__(self,  **kwargs):
        super(FlaskSecurityAdmin, self).__init__(**kwargs)

security = FlaskSecurityAdmin()
