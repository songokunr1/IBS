from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, TextAreaField, HiddenField, SelectMultipleField, SelectField, StringField,PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import DateNew,Category, Activity, Meal, User


def choices_by_category(*category):
    full_activity_list = Activity.list_of_activity_objects()
    return [(str(single.id), single.name) for single in full_activity_list if
            Category.find_by_id(single.category_id).category in [*category]]

class DateActivityReport(FlaskForm):
    box = BooleanField('Done or not!')
    date_id = HiddenField(validators=[DataRequired()])
    submit_done_or_not = SubmitField()


class ChooseDate(FlaskForm):
    date_report = DateField('Date', format='%Y-%m-%d')
    submit_date = SubmitField()

class ChooseDateNewReport(FlaskForm):
    date_report = DateField('Date', format='%Y-%m-%d')
    submit_date_new_report = SubmitField()


class FilterField(FlaskForm):
    filter = TextAreaField('filter', validators=[DataRequired()], default='')
    submit_filter = SubmitField()


class ChooseTypeAndDate(FlaskForm):
    date_report = DateField('Date', format='%Y-%m-%d')
    choices = [(type_of_report, type_of_report) for type_of_report in DateNew.list_of_types()]
    type_of_report = SelectField(u'Type to report',
                               choices=choices)
    submit_type_and_date = SubmitField()

class CreateMeal(FlaskForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        full_activity_list = Activity.list_of_activity_objects()
        self.ingredients.choices = [(str(single['id']), single['name']) for single in Activity.find_activities_by_x_category('białka mleka','cukier','laktoza','inne')]
# Meal.json_meal()
        self.meat_ingredients.choices = choices_by_category('wysoko białkowe')
        self.carbs_ingredients.choices = choices_by_category('wysoko weglowodanowe', 'bezglutenowe', 'gluten')
        self.warzywa_ingredients.choices = choices_by_category('warzywa', 'owoce')
    meal_name = StringField('meal_name')
    meat_ingredients = SelectMultipleField(u'meat_ingredients')
    carbs_ingredients = SelectMultipleField(u'wegle')
    warzywa_ingredients = SelectMultipleField(u'warzywa')
    ingredients = SelectMultipleField(u'ingredients')
    submit_meal = SubmitField()


class UpdateCategory(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_cat = Category.json_all()
        self.category_category_id.choices = [(single['id'], single['name']) for single in self.all_cat]

    category_category_id = SelectField('Type', coerce=int)
    category_name = TextAreaField('Name')
    submit_updated_category = SubmitField()

class UpdateActivity(FlaskForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_cat = Category.json_all()
        self.activity_category_id.choices = [(single['id'], single['name']) for single in self.all_cat]
        self.all_act = Activity.json_all()
        self.activity_activity_id.choices = [(single['id'], single['name']) for single in self.all_act]


    activity_category_id = SelectField('Type', coerce=int)
    activity_activity_id = SelectField('Type', coerce=int)
    box = BooleanField('Do you want to change category?', default=False)
    activity_name = TextAreaField('new activity name')

    submit_updated_activity = SubmitField()



class AddActivity(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_cat = Category.json_all()
        self.category_id.choices = [(single['id'], single['name']) for single in self.all_cat]

    category_id = SelectField('Type', coerce=int)
    activity_name = TextAreaField('new_activity')
    submit_new_activity = SubmitField()

class AddCategory(FlaskForm):
    category_name = TextAreaField('new_category')
    submit_new_category = SubmitField()

class DeleteActivity(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_cat = Activity.json_all()
        self.activity_id.choices = [(single['id'], single['name']) for single in self.all_cat]
    activity_id = SelectField('Type', coerce=int)
    submit_delete_activity = SubmitField()

class DeleteCategory(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_cat = Category.json_all()
        self.category_id.choices = [(single['id'], single['name']) for single in self.all_cat]
    category_id = SelectField('Type', coerce=int)
    submit_delete_category = SubmitField()

class DeleteMeal(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_meals = Meal.json_meal()
        self.meal_id.choices = [(single['id'], single['name']) for single in self.all_meals]
    meal_id = SelectField('Type', coerce=int)
    submit_delete_meal = SubmitField()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



# class ChooseMultiple(FlaskForm):
#     filter = FilterField
#     Filter_string = 'mleko'  #ta wartość powinna być zbierana przez FlaskForm <<
#     #Activity.filer_activity_objects()
#     choice = [(Category.query.filter_by(
#         category=category_name).first().id, category_name) for category_name in category_list]
#     language = SelectMultipleField(u'Programming Language',
#                                        choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
#     submit = SubmitField()

# class CompanyForm(FlaskForm):
#     company_name = StringField('company_name')
#     locations = FieldList(FormField(ChooseMultiple), min_entries=2)

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
