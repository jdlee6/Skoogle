from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    location = StringField('Enter City or Zip Code Below', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Search')