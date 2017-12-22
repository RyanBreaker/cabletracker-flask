from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login


#
# Abstract Models
#

class IdModel:
    id = db.Column(db.Integer, primary_key=True)


class BaseModel(IdModel):
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False, default='')

    def __repr__(self):
        return self.name


#
# User Model
#

class User(IdModel, UserMixin, db.Model):
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    @login.user_loader
    def load_user(cls, id_):
        return cls.query.get(int(id_))


#
# Tracking Models
#

class Cable(BaseModel, db.Model):
    __tablename__ = 'Cables'

    termination_a = db.Column(db.Integer, db.ForeignKey('termination.id'), index=True, nullable=False)
    termination_b = db.Column(db.Integer, db.ForeignKey('termination.id'), index=True, nullable=False)

    @property
    def serial(self):
        return '{0:06x}'.format(self.id)


class Termination(BaseModel, db.Model):
    __tablename__ = 'Terminations'

    termination_device = db.Column(db.Integer, db.ForeignKey('termination_device.id'), index=True, nullable=False)


class TerminationDevice(BaseModel, db.Model):
    __tablename__ = 'TerminationDevices'

    rack = db.Column(db.Integer, db.ForeignKey('rack.id'), index=True, nullable=False)
    unit = db.Column(db.SmallInteger, nullable=False, default=42)
    type = db.Column(db.Integer, db.ForeignKey('termination_device_type.id'), index=True)


class TerminationDeviceType(BaseModel, db.Model):
    __tablename__ = 'TerminationDeviceTypes'


class Rack(BaseModel, db.Model):
    room = db.Column(db.Integer, db.ForeignKey('room.id'), index=True, nullable=False)


class Room(BaseModel, db.Model):
    pass
