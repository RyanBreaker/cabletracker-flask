from flask import flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


def objects_for_selectfield(model):
    object_list = []
    all_objects = model.query.all()
    for object_ in all_objects:
        object_list += [(object_.id, object_.name)]
    return object_list


class BaseForm(FlaskForm):
    """
    Basic form for models that only have name and description columns.
    Can also be inherited by other forms that need to use name, description,
    and submit Fields.
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')

    def name_exists(self, object_, model):
        if self.name.data.lower() != object_.name.lower():
            if model.query.filter(model.name.ilike(self.name.data)).first() is not None:
                return True
        return False


class BaseDeleteForm(FlaskForm):
    confirm = SubmitField('Delete')
