from app import db
from app.models.base import BaseModel


#
# Tracking Models
#

class Cable(BaseModel):
    __tablename__ = 'Cables'

    termination_a = db.Column(db.Integer, db.ForeignKey('Terminations.id'), index=True, nullable=False)
    termination_b = db.Column(db.Integer, db.ForeignKey('Terminations.id'), index=True, nullable=False)

    @property
    def serial(self):
        return '{0:06x}'.format(self.id)

    @classmethod
    def from_serial(cls, serial):
        id_ = int(serial, 16)
        return cls.query.get(id_)


class Termination(BaseModel):
    __tablename__ = 'Terminations'

    termination_device = db.Column(db.Integer, db.ForeignKey('TerminationDevices.id'), index=True, nullable=False)


class TerminationDevice(BaseModel):
    __tablename__ = 'TerminationDevices'

    rack = db.Column(db.Integer, db.ForeignKey('Racks.id'), index=True, nullable=False)
    unit = db.Column(db.SmallInteger, nullable=False, default=42)
    type = db.Column(db.Integer, db.ForeignKey('TerminationDeviceTypes.id'), index=True, nullable=False)


class TerminationDeviceType(BaseModel):
    __tablename__ = 'TerminationDeviceTypes'


class Rack(BaseModel):
    __tablename__ = 'Racks'

    room = db.Column(db.Integer, db.ForeignKey('Rooms.id'), index=True, nullable=False)
    units = db.Column(db.SmallInteger, nullable=False, default=42)


class Room(BaseModel):
    __tablename__ = 'Rooms'
