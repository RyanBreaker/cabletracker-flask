from app import db


#
# Abstract Base Models
#

class IdModel:
    id = db.Column(db.Integer, primary_key=True)


class BaseModel(IdModel):
    name = db.Column(db.String(32), unique=True, nullable=False)
    description = db.Column(db.String, default=db.null)

    def __repr__(self):
        return self.name
