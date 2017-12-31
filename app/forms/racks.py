from wtforms import SelectField
from wtforms.validators import DataRequired

from app.forms import BaseForm
from app.forms.base import objects_for_selectfield
from app.models.tracking import Room


class RackForm(BaseForm):
    room = SelectField('Room', choices=objects_for_selectfield(Room), validators=[DataRequired()])
