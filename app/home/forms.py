from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, Record

class RecordForm(FlaskForm):
    """
    Form for workers to add or add Records
    """

    name = StringField('Name', validators = [DataRequired()])
    day = DateField('Date', validators = [DataRequired()])
    production = IntegerField('production', validators = [DataRequired()] )
    opening = IntegerField('opening count', validators = [DataRequired()] )
    closing = IntegerField('closing count', validators = [DataRequired()] )

    submit = SubmitField('Submit')
