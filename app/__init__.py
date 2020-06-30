import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:hattrick@localhost/ibs')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['WTF_CSRF_ENABLED'] = False

CORS(app, resources={r'/*': {'origins': '*'}})
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session = Session(engine)

csrf = CsrfProtect()
from app import routes

@app.before_first_request
def create_tables():
    db.create_all()