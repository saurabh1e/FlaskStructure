from flask import jsonify, request, make_response
from src import api, BaseResource, db
from .models import UserProfile, User
from .schemas import UserSchema, UserProfileSchema


class UserResource(BaseResource):

    model = User
    schema = UserSchema

    def get(self, slug):

        user = self.model.query.get(slug)
        if not user:
            return make_response(jsonify({'error': 100, 'message': 'User not found'}), 404)
        user_dump = self.schema(exclude=('username',)).dump(user).data
        db.session.commit()

        return jsonify({'success': 200, 'data': user_dump})

    def put(self, slug):

        user = self.model.query.get(slug)
        if not user:
            return make_response(jsonify({'error': 100, 'message': 'User not found'}), 404)
        user, errors = self.schema().load(instance=user)
        if errors:
            return make_response(jsonify({'error': 101, 'message': str(errors)}), 403)
        db.session.commit()

        return jsonify({'success': 200, 'message': 'user updated successfully', 'data': self.schema(exclude=('username',)).dump(user).data})

    def delete(self, slug):

        is_deleted = self.model.query.delete(slug)
        if not is_deleted:
            return make_response(jsonify({'error': 102, 'message': 'user deletion failed'}))
        db.session.commit()
        return jsonify({'success': 200, 'message': 'user deleted successfully'})


class UserListResource(BaseResource):

    model = User
    schema = UserSchema

    def get(self):
        users = self.model.query
        for key in request.args:
            if hasattr(self.model, key):
                values = request.args.getlist(key)  # one or many
                users = users.filter(getattr(self.model, key).in_(values))
        if 'page' not in request.args:
            resources = users.all()
        else:
            resources = users.paginate(
                int(request.args['page'])).items
        return jsonify({'success': 200, 'data': self.schema(exclude=('username',)).dump(resources, many=True)})

    def post(self):
        user, errors = self.schema().load(request.json, session=db.session)
        if errors:
            db.session.rollback()
            return make_response(jsonify({'error': 101, 'message': str(errors)}), 403)
        db.session.add(user)
        db.session.commit()
        user_count = self.model.query.filter(self.model.school_id == user.school_id).count()
        user.username = user.user_type[3] + (str(user.school_id) + str(user_count)).rjust(5, '0')
        db.session.commit()

        return jsonify({'success': 200, 'message': 'user added successfully',
                        'data': self.schema(exclude=('username',)).dump(user).data})


api.add_resource(UserListResource, '/users/', endpoint='users')
api.add_resource(UserResource, '/user/<string:slug>/', endpoint='user')


class UserProfileResource(BaseResource):

    model = UserProfile
    schema = UserProfileSchema

    def get(self, slug):

        user_profile = self.model.query.get(slug)
        if not user_profile:
            return make_response(jsonify({'error': 100, 'message': 'User Profile not found'}), 404)
        user_profile_dump = self.schema().dump(user_profile).data
        db.session.commit()

        return jsonify({'success': 200, 'data': user_profile_dump})

    def put(self, slug):

        user_profile = self.model.query.get(slug)
        if not user_profile:
            return make_response(jsonify({'error': 100, 'message': 'User Profile not found'}), 404)
        user_profile, errors = self.schema().load(instance=user_profile)
        if errors:
            return make_response(jsonify({'error': 101, 'message': str(errors)}), 403)
        db.session.commit()

        return jsonify({'success': 200, 'message': 'user_profile updated successfully', 'data': self.schema().dump(user_profile).data})

    def delete(self, slug):

        is_deleted = self.model.query.delete(slug)
        if not is_deleted:
            return make_response(jsonify({'error': 102, 'message': 'user_profile deletion failed'}))
        db.session.commit()
        return jsonify({'success': 200, 'message': 'user_profile deleted successfully'})


class UserProfileListResource(BaseResource):

    model = UserProfile
    schema = UserProfileSchema

    def get(self):
        user_profiles = self.model.query
        for key in request.args:
            if hasattr(self.model, key):
                values = request.args.getlist(key)  # one or many
                user_profiles = user_profiles.filter(getattr(self.model, key).in_(values))
        if 'page' not in request.args:
            resources = user_profiles.all()
        else:
            resources = user_profiles.paginate(
                int(request.args['page'])).items
        return jsonify({'success': 200, 'data': self.schema().dump(resources, many=True)})

    def post(self):

        user_profile, errors = self.schema().load(request.json, session=db.session)
        if errors:
            return make_response(jsonify({'error': 101, 'message': str(errors)}), 403)
        db.session.commit()
        return jsonify({'success': 200, 'message': 'user_profile added successfully', 'data': self.schema().dump(user_profile).data})

api.add_resource(UserProfileResource, '/user_profile/<string:slug>/', endpoint='user_profile')
api.add_resource(UserProfileListResource, '/user_profiles/', endpoint='user_profiles')
