from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    location = StringField('City or Zip Code', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Submit')