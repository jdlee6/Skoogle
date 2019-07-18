from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


# search form for home page
class SearchForm(FlaskForm):
    location = StringField('Enter the city or zip code below:', validators=[DataRequired(), Length(min=4)])
    radius = StringField('Enter the amount of miles below:', validators=[DataRequired(), Length(min=1, max=2)])
    submit = SubmitField('Search')