from hashlib import md5
from src.utils.serializer_helper import serialize_data
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import RoleMixin, UserMixin
from src import db, BaseMixin, ReprMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class UserName(db.Model, ReprMixin, BaseMixin):
    name = db.Column(db.String(127), nullable=True)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, BaseMixin, UserMixin, ReprMixin):
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), default='', nullable=False)
    username = db.Column(db.String(127), nullable=True)
    user_type = db.Column(db.Enum('student', 'counsellor'), default='counsellor')
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))

    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())

    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @staticmethod
    def hash_md5(data):
        return md5(data.encode('utf-8')).hexdigest()

    def get_auth_token(self):
        pass

    def generate_auth_token(self):
        token = serialize_data([str(self.id), self.hash_md5(self.password)])
        return token

    @hybrid_property
    def authentication_token(self):
        return self.generate_auth_token()

    @hybrid_property
    def name(self):
        if self.user_profile and self.user_profile.first_name:
            if self.user_profile.last_name:
                return self.user_profile.first_name + self.user_profile.last_name
            return self.user_profile.first_name


class UserProfile(db.Model, BaseMixin):
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.Enum('male', 'female', 'ns'), default='ns')
    dob = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    profile_picture = db.Column(db.String(512), nullable=True)
    address = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', lazy='subquery', backref='user_profile')

    @hybrid_property
    def age(self):
        if self.dob:
            return datetime.now().year - self.dob.year
        else:
            return 0


class School(db.Model, BaseMixin, ReprMixin):
    name = db.Column(db.String(127), nullable=False, unique=True)

    users = db.relationship('User', uselist=True, lazy='dynamic', backref='school')

    def generate_code(self, user_type):
        return serialize_data([self.id, user_type])

    @hybrid_property
    def school_counsellors(self):
        counsellors = User.query.filter(User.user_type == 'counsellor', User.school_id == self.id).all()
        return counsellors


class Chat(db.Model, BaseMixin):
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text(), nullable=False, default='')
    is_read = db.Column(db.Boolean(False))
    read_on = db.Column(db.TIMESTAMP, default=None)

    sender = db.relationship('User', lazy='subquery', foreign_keys=[sender_id])
    receiver = db.relationship('User', lazy='subquery', foreign_keys=[receiver_id])
