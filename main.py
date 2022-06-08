"""
Main module of the framework. Imports a URL-routes object, front
controller objects and the main Application object, then starts
a WSGI server.
"""
from wsgiref.simple_server import make_server

# from views import * - this import MUST be here otherwise the views.py
# file isn't initialized with the main.py file and the routes aren't added.
# if this import is missing, you MUST add it after this line!
from views import *
from core.wsgi_core import Application, LoggingApplication, SpoofApplication
from core.front_controllers import front_controller
from core.decorators import UrlPaths

routes = UrlPaths()

controllers = [
    front_controller
]
# Main application for the framework
application = Application(routes.URLS, controllers)

"""
Two spoof applications you may use for various purposes. Simply comment out
the real application above and uncomment either of the below applications.
The first one is a logging variation - it does everything exactly the same
with the exception of logging all the requests in stdout. The second one
is a dummy application, that only returns one phrase. Can be used for quick
testing of your URL routes.
"""
# application = LoggingApplication(routes.URLS, controllers)
# application = SpoofApplication(routes.URLS, controllers)

with make_server('127.0.0.1', 8000, application) as httpd:
    print('Running HTTP-server on port 8000...')
    httpd.serve_forever()
