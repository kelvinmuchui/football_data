from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Team


class TeamForm(FlaskForm):
    """
    Form for admin to add or edit a teams
    """
    name = StringField('Name', validators=[DataRequired()])
    history = StringField('History', validators=[DataRequired()])
    submit = SubmitField('Submit')
class PlayerForm(FlaskForm):
    """
    Form for admin to add or edit a player
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
class PlayerAssignForm(FlaskForm):
    """
    From for addmin to assign a team to PlayerAssignForm
    """
    team = QuerySelectField(query_factory = lambda : Team.query.all(),
                                get_label = "name")
    submit = SubmitField('Submit')
