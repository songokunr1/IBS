from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, widgets, FormField, FieldList, IntegerField,HiddenField
from wtforms_components import DateRange
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Category
from app.resources import Category_resources
from datetime import datetime, date
from wtforms.fields.html5 import DateField


class DateActivityReport(FlaskForm):
    box = BooleanField('Done or not!')
    date_id = HiddenField(validators=[DataRequired()])
    submit_done_or_not = SubmitField()

class ChooseDate(FlaskForm):
    date_report = DateField('Date', format='%Y-%m-%d')
    submit_date = SubmitField()

# class New_category(FlaskForm):
#     category = StringField('Category', validators=[DataRequired()])
#     box = BooleanField('Done')
#     submit = SubmitField()
#
#
# class New_habit(FlaskForm):
#     category_list = Category.list_of_category()
#     choice = [(Category.query.filter_by(
#         category=category_name).first().id, category_name) for category_name in category_list]
#     priority_list = ['High', 'Medium', 'Low']
#     priority_choices = [(prio,prio) for prio in priority_list]
#     name = TextAreaField('Name', validators=[DataRequired()])
#     category_type = SelectField('Type', coerce=int, validators=[DataRequired()], choices=choice)
#     start_date = DateField('start_date', format='%Y-%m-%d', validators=[DateRange(min=date.today())])
#     end_date = DateField('end_date', format='%Y-%m-%d', validators=[DateRange(min=date.today())])
#     priority = SelectField('priority', choices=(priority_choices))
#
#     submit = SubmitField()
#
#
# class Building_habit(FlaskForm):
#     box = BooleanField('Done or not!')
#     date_id = HiddenField(validators=[DataRequired()])
#
#     submit_done_or_not = SubmitField()
#
# class Delete_habit(FlaskForm):
#     category_list = Category.list_of_category()
#     choice = [(Category.query.filter_by(
#         category=category_name).first().id, category_name) for category_name in category_list]
#     category_type = SelectField('Type', coerce=int, validators=[DataRequired()], choices=choice)
#     submit_delete = SubmitField()
#
# class DateHabitReport(FlaskForm):
#     selected_date = DateField('start_date', format='%Y-%m-%d')
#     submit = SubmitField()
#
#
# class ExpensesForm(FlaskForm):
#     """A collection of expense items."""
#     items = FieldList(FormField(Building_habit), min_entries=1)