from datetime import datetime

from sqlalchemy.orm import backref

from app import db, login_manager
from flask_login import UserMixin, current_user
from sqlalchemy.dialects.postgresql.json import JSONB
import json
from psycopg2.extensions import register_adapter
import pandas as pd

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None



class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), unique=False, nullable=False)
    activity = db.relationship('Activity', lazy='dynamic', cascade='all,delete')
    dates = db.relationship('Date', lazy='dynamic', cascade='all,delete')
    datesnew = db.relationship("DateNew", lazy='dynamic', cascade='all,delete')
    username_id = db.Column(db.Integer, default=load_user(current_user))


    #
    # def __repr__(self):
    #     return self.id, self.category

    def __getitem__(self, index):
        return self.category

    def json(self):
        return {'name': self.category,
                'id': self.id}

    @classmethod
    def json_all(cls):
        cls.query.all()
        return [{'name': single.category,
                 'id': single.id} for single in cls.query.filter_by(username_id=current_user.id).all()]

    @classmethod
    def json_symptoms(cls):
        cls.query.all()
        return [{'name': single.category,
                 'id': single.id} for single in cls.query.filter_by(username_id=current_user.id).all()
                if single.category in ['objawy', 'stres', 'uzywki']]

    def json_meals(cls):
        cls.query.all()
        return [{'name': single.category,
                 'id': single.id} for single in cls.query.filter_by(username_id=current_user.id).all()
                if single.category not in ['objawy', 'stres', 'uzywki']]

    # __getitem__
    # __setitem__
    # __delitem__
    # def __setitem__(self, index, value):
    #     self.bricks.bricksId[index] = value
    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category, username_id=current_user.id).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id, username_id=current_user.id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(category= name, username_id=current_user.id).first()

    @classmethod
    def delete_all_objects_by_current_user(cls):
        cls.query.filter_by(username_id=current_user.id).delete()
        db.session.commit()


    @classmethod
    def find_name_by_id(cls, _id):
        return cls.query.filter_by(id=_id, username_id=current_user.id).first().category

    @classmethod
    def list_of_ids(cls):
        return cls.query.filter_by(username_id=current_user.id).all()

    @classmethod
    def list_of_category_objects(cls):
        return [single_category for single_category in cls.query.filter_by(username_id=current_user.id).all()]

    @staticmethod
    def list_of_category():
        return [single.category for single in Category.query.filter_by(username_id=current_user.id).all()]

    @staticmethod
    def list_of_not_meal_category():
        return ['stres', 'leki', 'objawy']

    @classmethod
    def list_of_meal_category(cls):
        return [single for single in cls.list_of_category() if single not in cls.list_of_not_meal_category()]

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    # type = db.Column(db.String(50), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    date_id = db.relationship("Date", back_populates="activity", cascade='all,delete')
    datenew_id = db.relationship("DateNew", lazy='dynamic', cascade='all,delete')
    username_id = db.Column(db.Integer, default=load_user(current_user))

    # def __init__(self, name=None, date_start=None, date_end=None, priority=None, category_id=None):
    #     self.data = (name, date_start, date_end, priority, category_id)

    def __repr__(self):
        return f"User('{self.name}')"

    @classmethod
    def list_of_dict_category_to_activities(cls):
        return [{Category.find_by_id(cls.find_by_name(single).category_id).category: single} for single in
                cls.list_of_activity()]

    @classmethod
    def json_all(cls):
        cls.query.all()
        return [{'name': single.name,
                 'id': single.id,
                 'category_id': single.category_id,
                 'category_name': Category.find_name_by_id(single.category_id)} for single in cls.query.filter_by(username_id=current_user.id).all()]

    @classmethod
    def json_symptoms(cls):
        cls.query.all()
        return [{'name': single.name,
                 'id': single.id,
                 'category_id': single.category_id,
                 'category_name': Category.find_name_by_id(single.category_id)} for single in cls.query.filter_by(username_id=current_user.id).all()
                if Category.find_name_by_id(single.category_id) in ['objawy', 'stres', 'uzywki', 'leki']]


    @classmethod
    def delete_all_objects_by_current_user(cls):
        cls.query.filter_by(username_id=current_user.id).delete()
        db.session.commit()


    @classmethod
    def find_activities_by_x_category(cls, *args):
        cls.query.all()
        return [{'name': single.name,
                 'id': single.id,
                 'category_id': single.category_id,
                 'category_name': Category.find_name_by_id(single.category_id)} for single in cls.query.filter_by(username_id=current_user.id).all()
                if Category.find_name_by_id(single.category_id) in [*args]]

#TODO: you are giving X arguments > and we getting dictionary with all activies within that category_args
    @classmethod
    def json_meals(cls):
        cls.query.filter_by(username_id=current_user.id).all()
        return [{'name': single.name,
                 'id': single.id,
                 'category_id': single.category_id,
                 'category_name': Category.find_name_by_id(single.category_id)} for single in cls.query.filter_by(username_id=current_user.id).all()
                if Category.find_name_by_id(single.category_id) not in ['objawy', 'stres', 'uzywki', 'leki']]

    @staticmethod
    def list_of_activity():
        return [single.name for single in Activity.query.filter_by(username_id=current_user.id).all()]

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id, username_id=current_user.id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name, username_id=current_user.id).first()

    @classmethod
    def find_name_by_id(cls, _id):
        data = cls.query.filter_by(id=_id, username_id=current_user.id).first()
        if data:
            return cls.query.filter_by(id=_id, username_id=current_user.id).first().name
        else:
            return None

    @classmethod
    def find_by_category_id(cls, _category_id):
        return cls.query.filter_by(category_id=_category_id, username_id=current_user.id).all()

    @classmethod
    def list_of_activity_objects(cls):
        return [single_activity for single_activity in cls.query.filter_by(username_id=current_user.id).all()]

    @classmethod
    def filer_activity_objects(cls, charts):
        return [single_activity for single_activity in cls.query.filter_by(username_id=current_user.id).all() if charts in single_activity.name.lower()]

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        print('I will try to delete')
        db.session.delete(self)
        print('I deleted!')
        db.session.commit()
        print('I commited session!')



class Date(db.Model):
    __tablename__ = 'date'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'),
                            nullable=False)
    activity = db.relationship('Activity',
                               primaryjoin='Activity.id == Date.activity_id',
                               backref=backref('Activity.name', lazy='joined', cascade='all,delete'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id')
                            , nullable=False)
    category = db.relationship('Category',
                               primaryjoin='Category.id == Date.category_id', lazy='joined')

    # activity jest obiektem modelu activity!
    def __repr__(self):
        return f"Date('{self.date}', '{self.activity}')"

    def json(self):
        # TODO add self.done
        return {'name': self.date, 'price': self.activity.name}

    @classmethod
    def list_of_date_objects(cls):
        return [single_activity for single_activity in cls.query.all()]

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_dates_by_activity_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_activitys_by_date(cls, _date):
        return cls.query.filter_by(date=_date).all()

    @classmethod
    def find_date_by_activity_id_and_date(cls, _id, date):
        return cls.query.filter_by(activity_id=_id, date=date).all()

    @classmethod
    def find_date_by_category_id_and_date(cls, _id, date):
        return cls.query.filter_by(category_id=_id, date=date).all()

    @classmethod
    def find_date_by_date_id_and_date(cls, _id, date):
        return cls.query.filter_by(id=_id, date=date).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class DateNew(db.Model):
    __tablename__ = 'datenew'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=True)
    breakfast = db.Column(db.Boolean, default=False)
    lunch = db.Column(db.Boolean, default=False)
    last_meal = db.Column(db.Boolean, default=False)
    morning = db.Column(db.Boolean, default=False)
    night = db.Column(db.Boolean, default=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'),
                            nullable=False)
    activity = db.relationship('Activity',
                               primaryjoin='Activity.id == DateNew.activity_id', lazy='joined', cascade='all,delete')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id')
                            , nullable=False)
    category = db.relationship('Category',
                               primaryjoin='Category.id == DateNew.category_id', lazy='joined', cascade='all,delete')
    username_id = db.Column(db.Integer, default=load_user(current_user))



    # activity jest obiektem modelu activity!
    def __repr__(self):
        return f"DateNew('{self.date}', '{self.activity}')"

    @classmethod
    def set_true_for_type_of_raport(cls, type):
        type_true_or_false = {single: (True if single == type else False) for single in
                              ['breakfast', 'lunch', 'last_meal', 'morning', 'night']}
        return type_true_or_false

    @classmethod
    def json_date(cls):
        return [{'id': date_object.id,
                 'date': date_object.date,
                 'done': date_object.done,
                 'breakfast': date_object.breakfast,
                 'lunch': date_object.lunch,
                 'last_meal': date_object.last_meal,
                 'morning': date_object.morning,
                 'night': date_object.night,
                 'activity_id': date_object.activity_id,
                 'category_id': date_object.category_id,
                 'username_id': date_object.username_id
                 }
                for date_object in cls.query.all()]

    @staticmethod
    def json_from_object(date_object):
        return { 'id': date_object.id,
                 'date': date_object.date,
                 'done': date_object.done,
                 'breakfast': date_object.breakfast,
                 'lunch': date_object.lunch,
                 'last_meal': date_object.last_meal,
                 'morning': date_object.morning,
                 'night': date_object.night,
                 'activity_id': date_object.activity_id,
                 'category_id': date_object.category_id,
                 'username_id': date_object.username_id
                 }

    @staticmethod
    def give_me_done_type_by_object(single_object):
        if single_object.breakfast:
            return 'breakfast'
        if single_object.lunch:
            return 'lunch'
        if single_object.last_meal:
            return 'last_meal'
        if single_object.morning:
            return 'morning'
        if single_object.night:
            return 'night'


    @classmethod
    def json_full_info_by_date(cls, today):
        return [{'id': date_object.id,
                 'date': date_object.date,
                 'done': date_object.done,
                 'breakfast': date_object.breakfast,
                 'lunch': date_object.lunch,
                 'last_meal': date_object.last_meal,
                 'morning': date_object.morning,
                 'night': date_object.night,
                 'activity_id': date_object.activity_id,
                 'category_id': date_object.category_id,
                 'activity_name': Activity.find_name_by_id(date_object.activity_id),
                 'category_name': Category.find_name_by_id(date_object.category_id),
                 'username_id': date_object.username_id
                 }
                for date_object in cls.find_activitys_by_date(today)]

    @classmethod
    def json_dict_list_of_done_activies_by_date(cls, today):
        list_of_done = {
         'breakfast_id': [],
         'lunch_id': [],
         'last_meal_id': [],
         'morning_id': [],
         'night_id': [],
         'breakfast_name': [],
         'lunch_name': [],
         'last_meal_name': [],
         'morning_name': [],
         'night_name': []
         }

        for date_object in cls.find_activitys_by_date(today):
            type = DateNew.give_me_done_type_by_object(date_object)
            list_of_done[type + '_id'].append(date_object.activity_id)
            list_of_done[type + '_name'].append(Activity.find_name_by_id(date_object.activity_id))
        return list_of_done


    @classmethod
    def list_of_types(cls):
        return ['breakfast', 'lunch', 'last_meal', 'morning', 'night']

    @staticmethod
    def json_of_types():
        return {'breakfast': 'meal', 'lunch': 'meal', 'last_meal': 'meal', 'morning': 'action', 'night': 'action'}

    @classmethod
    def list_of_date_objects(cls):
        return [single_activity for single_activity in cls.query.all()]

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id, username_id=current_user.id).first()

    @classmethod
    def find_dates_by_activity_id(cls, _id):
        return cls.query.filter_by(id=_id, username_id=current_user.id).first()

    @classmethod
    def find_activitys_by_date(cls, _date):
        return cls.query.filter_by(date=_date, username_id=current_user.id).all()

    @classmethod
    def delete_activitys_by_date(cls, _date):
        return cls.query.filter_by(date=_date, username_id=current_user.id).delete()

    @classmethod
    def find_activitys_by_date_and_type(cls, _date, breakfast=False, lunch=False, last_meal=False, morning=False,
                                        night=False):
        return cls.query.filter_by(date=_date, breakfast=breakfast, lunch=lunch, last_meal=last_meal, morning=morning,
                                   night=night, username_id=current_user.id).all()

    @classmethod
    def find_activitys_by_date_id_and_type(cls, _date, _id, breakfast=False, lunch=False, last_meal=False, morning=False,
                                        night=False):
        return cls.query.filter_by(date=_date, activity_id=_id, breakfast=breakfast, lunch=lunch, last_meal=last_meal, morning=morning,
                                   night=night,username_id=current_user.id).first()

    @classmethod
    def find_date_by_activity_id_and_date(cls, _id, date):
        return cls.query.filter_by(activity_id=_id, date=date, username_id=current_user.id).first()




    @classmethod
    def find_date_by_category_id_and_date(cls, _id, date):
        return cls.query.filter_by(category_id=_id, date=date, username_id=current_user.id).first()

    @classmethod
    def find_date_by_date_id_and_date(cls, _id, date):
        return cls.query.filter_by(id=_id, date=date, username_id=current_user.id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def add_to_db_by_list_and_type(cls, list_of_activities, type, chosen_date):
        for activity_id in list_of_activities:
            type_true_or_false = cls.set_true_for_type_of_raport(type)
            category_id = Category.find_by_id(Activity.find_by_id(activity_id).category_id).id
            today = DateNew(date=chosen_date, **type_true_or_false, category_id=category_id,
                            activity_id=activity_id, username=current_user.id)
            DateNew.save_to_db(today)
            # done_activite_ids = [single.activity_id for single in
            #                      DateNew.find_activitys_by_date_and_type(chosen_date, **type_true_or_false)]


    # @classmethod
    # def save_in_db_by_list_of_activities(cls,list_activity, date=chosen_date):
    #     for activity_id in list_activity:
    #         category_id = Category.find_by_id(Activity.find_by_id(activity_id).category_id).id
    #         today = DateNew(date=chosen_date, **type_true_or_false, category_id=category_id,
    #                         activity_id=activity_id)
    #         DateNew.save_to_db(today)
    #         flash('Your update has been created!', 'success')
    #         done_activite_ids = [single.activity_id for single in
    #                              DateNew.find_activitys_by_date_and_type(chosen_date, **type_true_or_false)]


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Meal(db.Model):
    __tablename__ = 'meal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(100), nullable=False)
    day_time = db.Column(db.String(20), default='lunch', nullable=False)
    username_id = db.Column(db.Integer, default=load_user(current_user))


    @classmethod
    def get_id(cls):
        return load_user(current_user)

    @classmethod
    def get_list_of_activities(cls, meal_ids):
        activity_ids = []
        for single_id in meal_ids:
            print(single_id)
            list_of_activity = Meal.find_list_of_ingredients_by_id(single_id)
            print([activity_ids.append(single_act_id) for single_act_id in list_of_activity if
             single_act_id not in activity_ids])
        return activity_ids

    @classmethod
    def find_by_id(cls, _id):
        meal = cls.query.filter_by(id=_id, username_id=current_user.id).first()
        if meal:
            return cls.query.filter_by(id=_id, username_id=current_user.id).first()
        else:
            return None
    @classmethod
    def get_list_of_activities_by_json(cls, meal_json):
        meal_ids_by_json = {'breakfast': [], 'lunch': [], 'last_meal': []}
        for each_time in ['breakfast', 'lunch', 'last_meal']:
            for single_id in meal_json[each_time]:
                print(single_id)
                list_of_activity = Meal.find_list_of_ingredients_by_id(single_id)
                print([meal_ids_by_json[each_time].append(single_act_id) for single_act_id in list_of_activity if
                 single_act_id not in meal_ids_by_json[each_time]])
        return meal_ids_by_json

    @classmethod
    def get_activities_by_time_of_meal_and_meal_id(cls, list_time_of_meal, list_meal_checkboxes):
        meal_ids_by_json = {'breakfast': [], 'lunch': [], 'last_meal': []}
        memory = 0
        for time_of_meal in list_time_of_meal:
            if time_of_meal == 'None':
                print('single, robie continue:', time_of_meal)
                continue
            print(list_time_of_meal, 'listtime')
            if time_of_meal == 'breakfast':
                meal_ids_by_json[time_of_meal].append(list_meal_checkboxes[memory])
            if time_of_meal == 'lunch':
                meal_ids_by_json[time_of_meal].append(list_meal_checkboxes[memory])
            if time_of_meal == 'last_meal':
                meal_ids_by_json[time_of_meal].append(list_meal_checkboxes[memory])
            memory += 1
        return Meal.get_list_of_activities_by_json(meal_ids_by_json)

    @classmethod
    def list_of_meals(cls):
        return [meal_object.name for meal_object in cls.query.filter_by(username_id=current_user.id).all()]

    @classmethod
    def json_meal(cls):
        return [{'id': meal_object.id,
                 'name': meal_object.name,
                 'ingredients': meal_object.ingredients,
                 'date_time': meal_object.day_time,
                 'list_of_ingredients_names': cls.list_of_activity_names_for_meal_id(meal_object.id)} for meal_object in
                cls.query.filter_by(username_id=current_user.id).all()]

    @classmethod
    def list_of_activity_ids_for_meal_id(cls, single_id):
        list_of_ingr = cls.find_list_of_ingredients_by_id(id)
        activity_ids = []
        [activity_ids.append(Activity.find_by_id(single_act_id).id) for single_act_id in list_of_ingr]
        return activity_ids

    @classmethod
    def list_of_activity_names_for_meal_id(cls, id):
        list_of_ingr = cls.find_list_of_ingredients_by_id(id)
        activity_ids = []
        [activity_ids.append(Activity.find_name_by_id(single_act_id)) for single_act_id in list_of_ingr]
        return activity_ids

    @classmethod
    def find_meal_by_name(cls, name):
        return cls.query.filter_by(name=name, username_id=current_user.id).first().name

    @classmethod
    def find_meal_by_name(cls, name):
        return cls.query.filter_by(name=name, username_id=current_user.id).first().name

    @classmethod
    def find_meal_by_id(cls, id):
        return cls.query.filter_by(id=id, username_id=current_user.id).first().name

    @classmethod
    def find_meal_by_id(cls, id):
        return cls.query.filter_by(id=id, username_id=current_user.id).first().name

    @classmethod
    def find_list_of_ingredients_by_id(cls, _id):
        all = cls.query.filter_by(id=_id, username_id=current_user.id).first().ingredients
        return all.split(',')

    @classmethod
    def find_list_of_ingredients_by_id(cls, id):
        all = cls.query.filter_by(id=id, username_id=current_user.id).first().ingredients
        return all.split(',')

    def find_string_of_ingredients_by_id(cls, _id):
        return cls.query.filter_by(id=_id, username_id=current_user.id).first().ingredients

    @classmethod
    def list_of_ingredients(cls, meal):
        magic_string = cls.find_meal_by_name(meal)
        list_of_ingredients_ids = magic_string.split(",")
        list_of_ingredients = [Activity.find_name_by_id(single_ingredient) for single_ingredient in
                               list_of_ingredients_ids]
        return list_of_ingredients

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def ingredients_for_meal(**ingredients):
        list_of_ingridients = [','.join(v) for k, v in ingredients.items() if v != []]
        full_string_ids = ','.join(list_of_ingridients)
        list_of_ingridients_names = []
        [list_of_ingridients_names.append(Activity.find_by_id(int(single)).name) for single in
         full_string_ids.split(',') if Activity.find_by_id(int(single)).name not in list_of_ingridients_names]
        print(list_of_ingridients_names)
        list_of_ingridients_ids = [Activity.find_by_name(name).id for name in list_of_ingridients_names]
        print(list_of_ingridients_ids)
        string_of_ingridients_ids = ','.join(str(x) for x in list_of_ingridients_ids)
        list_of_dict = [{'id': _id, 'name': _name} for _id, _name in
                        zip(list_of_ingridients_ids, list_of_ingridients_names)]
        return {'list_of_ingridients_ids': list_of_ingridients_ids,
                'list_of_ingridients_names': list_of_ingridients_names,
                'string_of_ingridients_ids': string_of_ingridients_ids, }


class Database:
    @staticmethod
    def list_of_ids(obj):
        list_of_id = []
        for i in db.session.query(obj.id).all():
            list_of_id.append(i[0])
        return list_of_id

    @staticmethod
    def list_of_column(obj, table, _id):
        list_of_col = []
        for i in obj.find_by_id(table, _id):
            list_of_col.append(i)
        return list_of_col

    @staticmethod
    def find_by_id(table, _id):
        return table.query.filter_by(id=_id).first()

    @staticmethod
    def column_with_id(table, column, _id):
        print(table.find_by_id(db.session.query(table._id).all()))


# class Stats(db.Model):
#     __tablename__ = 'stats'
#     id = db.Column(db.Integer, primary_key=True)
#     ip = db.Column(db.String(100), nullable=False)
#     country = db.Column(db.String(10), nullable=False)
#     location = db.Column(db.String(100), nullable=False)
#     date = db.Column(db.String(100), nullable=False)
#     visit = db.Column(db.Integer, default=1, nullable=False)
#
#     @classmethod
#     def data_json(cls):
#         return [{'id': stats_object.id,
#                  'ip': stats_object.ip,
#                  'country': stats_object.country,
#                  'location': stats_object.location,
#                  'date': stats_object.date,
#                  'visit': stats_object.visit} for stats_object in
#                 cls.query.all()]
#
#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()

class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    visits = db.Column(db.Integer, nullable=False)

    @classmethod
    def data_json(cls):
        return [{'id': stats_object.id,
                 'date': stats_object.date,
                 'visits': stats_object.visit} for stats_object in
                cls.query.all()]

    @classmethod
    def find_object_by_date(cls, _date):
        return cls.query.filter_by(date=_date).first()

    @classmethod
    def is_date_in_database(cls, _date):
        a = cls.query.filter_by(date=_date).scalar() is not None
        return a

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_object_by_date(cls, _date):
        return cls.query.filter_by(date=_date).first()


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Template(db.Model, UserMixin):
    __tablename__ = 'template'

    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(20), unique=True, nullable=False)
    json_template = db.Column(JSONB, nullable=False)
    # category = {'category': []}
    # activity = {'category_id'}


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    #TODO
    # backup category with activity(json_all)
    # add new record with category and activity
    # check id for specyfic category
    # get full json with category and activity and category_id
    # add activity to database from get_full_json


        # for single in instances:
        #     json_object.append({'category': single['category_name'],
        #                                      'activity': single['name']})
        #     record_category = Template(template_name=name, category=True, record_name=single['category_name'])
        #     record_activity = Template(template_name=name, activity=True, record_name=single['category_name'])
        #     db.session.add(record_category)
        #     db.session.add(record_activity)
        # db.session.commit()



    @classmethod
    def create_new_record_from_template(cls, name, instances):
        db.create_all()
        json_object = {'instances': []}
        # print(instances)
        for single in instances:
            json_object['instances'].append({'category': single['category_name'],
                                             'activity': single['name']})


        new = Template(template_name=name, json_template=json_object)
        cls.save_to_db(new)

    @classmethod
    def update_category_id_from_created_instance(cls):
        pass
    @classmethod
    def get_template_from_categories_and_activities_names(cls, instances):
        #TODO
        # add to database all categories and commit!
        # craete empty instance list
        # loop by tuple act and category // objects[{category:x, 'activity': b}]
        #  here you write find_category_id_by_cat_name
        #  adding to instance list
        return {
    "instances": [{
        "category_id": 1,
        "category": 2,
        "activity": 3
    }]
}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(template_name=name).first()

    #TODO
    # we have template, now we need to add it to liste category
