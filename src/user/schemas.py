from . import ma
from .models import User, UserProfile


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
        exclude = ('created_on', 'updated_on')

    id = ma.Integer(dump_only=True)
    password = ma.String(load_only=True)
    user_profile = ma.Nested('UserProfileSchema', many=False)


class UserProfileSchema(ma.ModelSchema):

    class Meta:
        model = UserProfile
        exclude = ('created_on', 'updated_on')

    id = ma.Integer(dump_only=True)
