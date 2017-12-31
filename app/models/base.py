from app import db


#
# Abstract Base Models
#

class IdModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class BaseModel(IdModel):
    __abstract__ = True

    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String, default=db.null)

    query = None

    def __repr__(self):
        return self.name

    @classmethod
    def name_exists(cls, name):
        return cls.query.filter(cls.name.ilike(name)).first() is not None
