from app import db
from app.models import Category, Activity, Date, DateNew, Meal

db.create_all()
db.session.add(Category(category='test_heroku'))

db.session.commit()