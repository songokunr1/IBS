import unittest
from app import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import DateNew, Category, Activity, Meal
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from unittest.mock import patch

class TestIBS(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls) -> None:
    #     app = Flask(__name__)
    #     app.config['TESTING'] = True
    #     app.config['DEBUG'] = False
    #     db = SQLAlchemy(app)
    #     engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    #     session = Session(engine)
    #     print('setupClass')
    #
    # @classmethod
    # def tearDownClass(cls) -> None:
    #     print('teardownClass')
    #
    # def setUp(self) -> None:
    #     print('setUp')
    # def tearDown(self) -> None:
    #     print('tearDown')

    def testCategory(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status= response.status_code
        self.assertEqual(status, 400)
if __name__ == '__main__':
    unittest.main()
