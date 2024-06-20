from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, DateField, BooleanField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    created_by = IntegerField('Created_by', validators=[DataRequired()])
    begin_at = DateField('Begin_at', validators=[DataRequired()])
    end_at = DateField('End_at', validators=[DataRequired()])
    max_users = IntegerField('Max_users', validators=[DataRequired()])
    is_active = BooleanField('Is_active', validators=[DataRequired()])
class EventUserForm(FlaskForm):
    user_id = IntegerField('User_id', validators=[DataRequired()])
    event_id = IntegerField('Event_id', validators=[DataRequired()])
    score = IntegerField('Score')
    created_at = DateField('Created_at', validators=[DataRequired()])