from app import app
from app import db

if __name__ == '__main__':
    app.run(port=8020, debug=True)


@app.before_first_request
def create_tables():
    db.create_all()
