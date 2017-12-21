from app import db


class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False, default='')


class Cable(db.Model, BaseModel):
    termination_a = db.Column(db.Integer, db.ForeignKey('termination.id'), nullable=False)
    termination_b = db.Column(db.Integer, db.ForeignKey('termination.id'), nullable=False)


class Termination(db.Model, BaseModel):
    rack = db.Column(db.Integer, db.ForeignKey('rack.id'), nullable=False)
    unit = db.Column(db.Integer, default=42, nullable=False)


class Rack(db.Model, BaseModel):
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.Text())

    @property
    def serial(self):
        return '{0:06x}'.format(self.id)
