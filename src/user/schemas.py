from marshmallow import pre_load, pre_dump

from src import ma
from src.utils.serializer_helper import deserialize_data
from .models import UserProfile, User, School, Chat


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
        exclude = ('created_on', 'updated_on', 'password', 'current_login_at', 'current_login_ip', 'last_login_at', 'last_login_ip',
                   'login_count')

    id = ma.Integer(dump_only=True)
    email = ma.Email()
    user_profile = ma.Nested('UserProfileSchema', many=False)
    school = ma.Nested('SchoolSchema', many=False)
    authentication_token = ma.String()

    @pre_load
    def save_model(self, in_data):
        deserialized_data = deserialize_data(in_data['school_code'])
        in_data['school_id'] = deserialized_data[0]
        in_data['user_type'] = deserialized_data[1]
        return in_data


class UserProfileSchema(ma.ModelSchema):

    class Meta:
        model = UserProfile
        exclude = ('created_on', 'updated_on', 'user')

    id = ma.Integer(dump_only=True)


class SchoolSchema(ma.ModelSchema):
    class Meta:
        model = School
        exclude = ('created_on', 'updated_on', 'users')

    id = ma.Integer(dump_only=True)
    school_counsellors = ma.Nested('UserSchema', exclude=('school',), many=True)


class ChatSchema(ma.ModelSchema):

    class Meta:
        model = Chat
        exclude = ('created_on', 'updated_on')

    id = ma.Integer(dump_only=True)
    sender = ma.Nested('UserSchema', only=('username',), many=False, dump_only=True)
    receiver = ma.Nested('UserSchema', only=('username',), many=False, dump_only=True)
