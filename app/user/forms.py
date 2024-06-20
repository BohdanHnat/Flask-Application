from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):
    first_name = StringField('First_name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last_name', validators=[DataRequired(), Length(min=1, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])