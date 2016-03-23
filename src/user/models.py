from . import db, ReprMixin


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), default='', nullable=False)

    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id', ondelete='CASCADE'))
    user_profile = db.relationship('UserProfile', uselist=False, foreign_keys=[user_profile_id], lazy='subquery')

    created_on = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_on = db.Column(db.TIMESTAMP, onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.id, self.email)


class UserProfile(db.Model, ReprMixin):

    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), default='New User', nullable=False)
    age = db.Column(db.SmallInteger(), default=0, nullable=True)
