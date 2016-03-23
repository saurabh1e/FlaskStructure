from flask import jsonify, request, make_response
from . import api, BaseResource, db
from .models import UserProfile, User
from .schemas import UserSchema, UserProfileSchema


class UserResource(BaseResource):

    model = User
    schema = UserSchema

    def get(self, slug):

        user = self.model.query.get(slug)
        if not user:
            return make_response(jsonify({'error': 100, 'message': 'User not found'}), 404)
        user_dump = self.schema().dump(user).data
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

        return jsonify({'success': 200, 'message': 'user updated successfully', 'data': self.schema().dump(user).data})

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

        return jsonify({'success': 200, 'data': 'data'})

    def post(self):

        user, errors = self.schema().load(request.json, session=db.session)
        if errors:
            return make_response(jsonify({'error': 101, 'message': str(errors)}), 403)
        db.session.commit()
        return jsonify({'success': 200, 'message': 'user added successfully', 'data': self.schema().dump(user).data})


api.add_resource(UserResource, '/user/<int:slug>/', endpoint='user')
