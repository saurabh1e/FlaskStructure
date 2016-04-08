from src import ma
from .models import UserProfile, User


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
        exclude = ('created_on', 'updated_on')

    id = ma.Integer(dump_only=True)
    email = ma.Email()


class UserProfileSchema(ma.ModelSchema):

    class Meta:
        model = UserProfile
        exclude = ('created_on', 'updated_on')

    id = ma.Integer(dump_only=True)
