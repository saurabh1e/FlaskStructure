from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import RoleMixin, UserMixin
from src import db, BaseMixin, ReprMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, BaseMixin, ReprMixin, UserMixin):

    name = db.Column(db.String(55), default='New User', nullable=False)
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), default='', nullable=False)

    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())

    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class UserProfile(db.Model, BaseMixin):

    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    dob = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    profile_picture = db.Column(db.String(512), nullable=True)
    address = db.Column(db.Integer)
    qualification = db.Column(db.Integer)

    @hybrid_property
    def age(self):
        return self.dob.year - datetime.now().year

