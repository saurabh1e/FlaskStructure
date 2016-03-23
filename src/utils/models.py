from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ReprMixin(object):
    """Provides a string representible form for objects."""

    __repr_fields__ = ['id', 'name']

    def __repr__(self):
        fields =  {f:getattr(self, f, '<BLANK>') for f in self.__repr_fields__}
        pattern = ['{0}={{{0}}}'.format(f) for f in self.__repr_fields__]
        pattern = ' '.join(pattern)
        pattern = pattern.format(**fields)
        return '<{} {}>'.format(self.__class__.__name__, pattern)
