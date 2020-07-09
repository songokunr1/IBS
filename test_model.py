import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import DateNew, Category, Activity, Meal
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

from unittest.mock import patch

class TestCategory(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        db = SQLAlchemy(app)
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        session = Session(engine)

        print('setupClass')

    @classmethod
    def tearDownClass(cls) -> None:
        print('teardownClass')

    def setUp(self) -> None:
        print('setUp')
        self.cat1 = Category('sport')
        self.act1 = Activity(name='bieganie', category_id = self.cat1.id)
        types = ['breakfast', 'lunch', 'last_meal', 'morning', 'night']
        arguments = {'breakfast': False,
                     'lunch': False,
                     'last_meal': False,
                     'morning': False,
                     'night': False}
        self.date = []
        for type in types:
            arguments[type]=True
            self.date.append(DateNew(date='2020-05-31', **arguments, category_id =self.cat1.id, activity_id = self.act1.id))
            arguments[type] = False

    def tearDown(self) -> None:
        print('tearDown')

    def testCategory(self):
        self.assertEqual(self.cat1.category, 'sport')
        self.assertEqual(self.cat1.category, 'sport')
    def testActivity(self):
        self.assertEqual(self.act1.name, 'bieganie')


    def test_NewDate(self):
        print('test NewDate')
        self.assertEqual(self.date[0].date, '2020-05-31')
        self.assertEqual(self.date[0].breakfast,  True)
        self.assertEqual(self.date[1].lunch,  True)
        self.assertEqual(self.date[2].last_meal,  True)
        self.assertEqual(self.date[3].morning,  True)
        self.assertEqual(self.date[4].night,  True)
        self.assertEqual(self.date[3].night,  False)




if __name__ == '__main__':
    unittest.main()
