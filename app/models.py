from datetime import datetime

from sqlalchemy.orm import backref

from app import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), unique=True, nullable=False)
    activity = db.relationship('Activity', lazy='dynamic')
    dates = db.relationship('Date', lazy='dynamic')

    def __init__(self, category):
        self.category = category

    #
    # def __repr__(self):
    #     return self.id, self.category

    def __getitem__(self, index):
        return self.category

    def json(self):
        return {'name': self.category}

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
        return [single_category.category for single_category in cls.query.all()]

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
    date_id = db.relationship("Date", back_populates="activity")

    # def __init__(self, name=None, date_start=None, date_end=None, priority=None, category_id=None):
    #     self.data = (name, date_start, date_end, priority, category_id)

    def __repr__(self):
        return f"User('{self.name}')"

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Date(db.Model):
    __tablename__ = 'date'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'),
                            nullable=False)
    activity = db.relationship('Activity',
                            primaryjoin='Activity.id == Date.activity_id',
                            backref=backref('Activity.name', lazy='joined'))
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
