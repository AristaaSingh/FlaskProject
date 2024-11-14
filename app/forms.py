from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import Assessment


class AssessmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    module_code = StringField('Module Code',
                              validators=[DataRequired(), Length(max=10)])
    deadline_date = DateTimeLocalField('Deadline Date',
                                       format='%Y-%m-%dT%H:%M',
                                       validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=500)])
    is_complete = BooleanField('Completed')
    submit = SubmitField('Save')
