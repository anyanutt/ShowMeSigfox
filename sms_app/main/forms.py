from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, SubmitField, DateField, DateTimeField, FormField
from wtforms.validators import ValidationError, DataRequired, InputRequired, EqualTo, Length

from sms_app.models import User, Device, Variable, Dashboard

class NewDeviceForm(FlaskForm):
    sigfox_id = StringField('Sigfox ID', validators=[DataRequired(), Length(min=6, max=8)])
    dev_name = StringField('Device Name', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_sigfox_id(self, sigfox_id):
        device = Device.get_by_sid(sid=sigfox_id.data.upper())
        if device is not None:
            raise ValidationError('This device is already registered on ShowMeSigfox')


class NewDashboardForm(FlaskForm):
    dash_name = StringField('Dashboard Name', validators=[DataRequired()])
    submit = SubmitField('Add')

class DateFilterForm(FlaskForm):
    date = DateField('date')
    datetime = DateTimeField('datetime')

class NewVariableForm(FlaskForm):
    var_name = StringField('Variable Name', validators=[DataRequired()])
    source = SelectField('Data Source', validators=[InputRequired()])
    aggregation = SelectField('Aggregation', choices=Variable.aggregation)
    unit = StringField('Unit')
    datefilter = BooleanField('Date/time filtering')
    submit = SubmitField('Add')

class NewWidgetForm(FlaskForm):
    name = StringField('Widget Name')
    source = SelectField('Choose Variables', choices=Dashboard.choices, validators=[InputRequired()])
    submit = SubmitField('Add')


