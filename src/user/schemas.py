from src import ma
from .models import UserProfile, User


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
        exclude = ('created_on', 'updated_on', 'password', 'current_login_at', 'current_login_ip',
                   'last_login_at', 'last_login_ip', 'login_count')

    id = ma.Integer(dump_only=True)
    email = ma.Email()
    user_profile = ma.Nested('UserProfileSchema', many=False)


class UserProfileSchema(ma.ModelSchema):

    class Meta:
        model = UserProfile
        exclude = ('created_on', 'updated_on', 'user')

    id = ma.Integer(dump_only=True)
