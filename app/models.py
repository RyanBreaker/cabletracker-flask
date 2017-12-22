from app import db


#
# Abstract Models
#

class IdModel:
    id = db.Column(db.Integer, primary_key=True)


class BaseModel(IdModel):
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False, default='')


#
# User Model
#

class User(IdModel, db.Model):
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


#
# Tracking Models
#

class Cable(BaseModel, db.Model):
    termination_a = db.Column(db.Integer, db.ForeignKey('termination.id'), nullable=False)
    termination_b = db.Column(db.Integer, db.ForeignKey('termination.id'), nullable=False)


class Termination(BaseModel, db.Model):
    rack = db.Column(db.Integer, db.ForeignKey('rack.id'), nullable=False)
    unit = db.Column(db.Integer, default=42, nullable=False)


class Rack(BaseModel, db.Model):
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.Text())

    @property
    def serial(self):
        return '{0:06x}'.format(self.id)
