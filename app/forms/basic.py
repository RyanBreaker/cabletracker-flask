from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


def get_models_for_choice_field(model):
    models_list = []
    all_models = model.query.all()
    for model in all_models:
        models_list += [(model.id, model.name)]
    return models_list


class CreateBasicForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')
