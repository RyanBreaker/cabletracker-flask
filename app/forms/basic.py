from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


def get_models_for_choice_field(model):
    models_list = []
    all_models = model.query.all()
    for model in all_models:
        models_list += [(model.id, model.name)]
    return models_list


class BasicForm(FlaskForm):
    """
    Basic form for models that only have name and description columns.
    Can also be inherited by other forms that need to use name, description,
    and submit Fields.
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class BasicDeleteForm(FlaskForm):
    confirm = SubmitField('Delete')
