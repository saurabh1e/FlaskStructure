# FlaskStructure

Flask Seed App pre configured with Flask-Security, Flask-Restful, Flask-Marshmallow, Flask-Sqlalchemy, Flask-Admin.

Instructions to run:

1. python manage.py db init
2. python manage.py db migrate
3. python manage.py db upgrade
4. python manage.py runserver

Note:

1. Create User, and associate 'admin' role with it to access endpoints
2. Login Url /test/v1//login

App is configured with flask security token based auth, after logging in you will receive a auth token
which has to be sent in every request in header with key authentication-token

App is configured to use factory method.

Sample User models, schemas and api is configured.

