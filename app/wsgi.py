from werkzeug.wsgi import DispatcherMiddleware

from app.dash.app1 import app as app1
from app.__init__ import app as flask_app
from app2 import app as app2

application = DispatcherMiddleware(flask_app, {
    '/app1': app1.server,
})