from app import app
from app import db
import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
#    app.run(port=8020, debug=True)


@app.before_first_request
def create_tables():
    db.create_all()
