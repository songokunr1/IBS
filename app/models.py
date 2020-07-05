from datetime import datetime

from sqlalchemy.orm import backref

from app import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), unique=True, nullable=False)
    activity = db.relationship('Activity', lazy='dynamic', cascade='all,delete')
    dates = db.relationship('Date', lazy='dynamic', cascade='all,delete')
    datesnew = db.relationship("DateNew", lazy='dynamic', cascade='all,delete')

    def __init__(self, category):
        self.category = category

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
                 'id': single.id} for single in cls.query.all()]

    @classmethod
    def json_symptoms(cls):
        cls.query.all()
        return [{'name': single.category,
                 'id': single.id} for single in cls.query.all()
                if single.category in ['objawy', 'stres', 'uzywki']]

    def json_meals(cls):
        cls.query.all()
        return [{'name': single.category,
                 'id': single.id} for single in cls.query.all()
                if single.category not in ['objawy', 'stres', 'uzywki']]

    # __getitem__
    # __setitem__
    # __delitem__
    # def __setitem__(self, index, value):
    #     self.bricks.bricksId[index] = value
    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_name_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first().category

    @classmethod
    def list_of_ids(cls):
        return cls.query.all()

    @classmethod
    def list_of_category_objects(cls):
        return [single_category for single_category in cls.query.all()]

    @staticmethod
    def list_of_category():
        return [single.category for single in Category.query.all()]

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
    name = db.Column(db.String(50), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    date_id = db.relationship("Date", back_populates="activity", cascade='all,delete')
    datenew_id = db.relationship("DateNew", lazy='dynamic', cascade='all,delete')

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
                 'category_name:': Category.find_name_by_id(single.category_id)} for single in cls.query.all()]

    @classmethod
    def json_symptoms(cls):
        cls.query.all()
        return [{'name': single.name,
                 'id': single.id,
                 'category_id': single.category_id,
                 'category_name': Category.find_name_by_id(single.category_id)} for single in cls.query.all()
                if Category.find_name_by_id(single.category_id) in ['objawy', 'stres', 'uzywki', 'leki']]

    @classmethod
    def find_activities_by_x_category(cls, *args):
        cls.query.all()
        return [{'name': single.name,
                 'id': single.id,
                 'category_id': single.category_id,
                 'category_name': Category.find_name_by_id(single.category_id)} for single in cls.query.all()
                if Category.find_name_by_id(single.category_id) in [*args]]

#TODO: you are giving X arguments > and we getting dictionary with all activies within that category_args
    @classmethod
    def json_meals(cls):
        cls.query.all()
        return [{'name': single.name,
                 'id': single.id,
                 'category_id': single.category_id,
                 'category_name': Category.find_name_by_id(single.category_id)} for single in cls.query.all()
                if Category.find_name_by_id(single.category_id) not in ['objawy', 'stres', 'uzywki', 'leki']]

    @staticmethod
    def list_of_activity():
        return [single.name for single in Activity.query.all()]

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_name_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first().name

    @classmethod
    def find_by_category_id(cls, _category_id):
        return cls.query.filter_by(category_id=_category_id).all()

    @classmethod
    def list_of_activity_objects(cls):
        return [single_activity for single_activity in cls.query.all()]

    @classmethod
    def filer_activity_objects(cls, charts):
        return [single_activity for single_activity in cls.query.all() if charts in single_activity.name.lower()]

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

    # activity jest obiektem modelu activity!
    def __repr__(self):
        return f"DateNew('{self.date}', '{self.activity}')"

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
                 'category_id': date_object.category_id
                 }
                for date_object in cls.query.all()]

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
                 'category_name': Category.find_name_by_id(date_object.category_id)
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
            if date_object.breakfast:
                list_of_done['breakfast_id'].append(date_object.activity_id)
                list_of_done['breakfast_name'].append(Activity.find_name_by_id(date_object.activity_id))
            if date_object.lunch:
                list_of_done['lunch_id'].append(date_object.activity_id)
                list_of_done['lunch_name'].append(Activity.find_name_by_id(date_object.activity_id))
            if date_object.last_meal:
                list_of_done['last_meal_id'].append(date_object.activity_id)
                list_of_done['last_meal_name'].append(Activity.find_name_by_id(date_object.activity_id))
            if date_object.morning:
                list_of_done['morning_id'].append(date_object.activity_id)
                list_of_done['morning_name'].append(Activity.find_name_by_id(date_object.activity_id))
            if date_object.night:
                list_of_done['night_id'].append(date_object.activity_id)
                list_of_done['night_name'].append(Activity.find_name_by_id(date_object.activity_id))
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
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_dates_by_activity_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_activitys_by_date(cls, _date):
        return cls.query.filter_by(date=_date).all()

    @classmethod
    def find_activitys_by_date_and_type(cls, _date, breakfast=False, lunch=False, last_meal=False, morning=False,
                                        night=False):
        return cls.query.filter_by(date=_date, breakfast=breakfast, lunch=lunch, last_meal=last_meal, morning=morning,
                                   night=night).all()

    @classmethod
    def find_activitys_by_date_id_and_type(cls, _date, _id, breakfast=False, lunch=False, last_meal=False, morning=False,
                                        night=False):
        return cls.query.filter_by(date=_date, activity_id=_id, breakfast=breakfast, lunch=lunch, last_meal=last_meal, morning=morning,
                                   night=night).first()

    @classmethod
    def find_date_by_activity_id_and_date(cls, _id, date):
        return cls.query.filter_by(activity_id=_id, date=date).first()




    @classmethod
    def find_date_by_category_id_and_date(cls, _id, date):
        return cls.query.filter_by(category_id=_id, date=date).first()

    @classmethod
    def find_date_by_date_id_and_date(cls, _id, date):
        return cls.query.filter_by(id=_id, date=date).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Meal(db.Model):
    __tablename__ = 'meal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(100), nullable=False)
    day_time = db.Column(db.String(20), default='lunch', nullable=False)

    @classmethod
    def list_of_meals(cls):
        return [meal_object.name for meal_object in cls.query.all()]

    @classmethod
    def json_meal(cls):
        return [{'id': meal_object.id,
                 'name': meal_object.name,
                 'ingredients': meal_object.ingredients,
                 'date_time': meal_object.day_time,
                 'list_of_ingredients_names': cls.list_of_activity_names_for_meal_id(meal_object.id)} for meal_object in
                cls.query.all()]

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
        return cls.query.filter_by(name=name).first().name

    @classmethod
    def find_meal_by_name(cls, name):
        return cls.query.filter_by(name=name).first().name

    @classmethod
    def find_meal_by_id(cls, id):
        return cls.query.filter_by(id=id).first().name

    @classmethod
    def find_meal_by_id(cls, id):
        return cls.query.filter_by(id=id).first().name

    @classmethod
    def find_list_of_ingredients_by_id(cls, _id):
        all = cls.query.filter_by(id=_id).first().ingredients
        return all.split(',')

    @classmethod
    def find_list_of_ingredients_by_id(cls, id):
        all = cls.query.filter_by(id=id).first().ingredients
        return all.split(',')

    def find_string_of_ingredients_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first().ingredients

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
