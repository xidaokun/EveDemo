from flask import Flask, request

from main import src
from main.settings import MODE_DEV

DEFAULT_APP_NAME = 'backend services'

app = Flask(DEFAULT_APP_NAME)


def create_service(mode=MODE_DEV):
    global app
    src.init_app(app, mode)
    return app


@app.before_request
def handle_chunking():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams; this makes the API
    compliant with the HTTP/1.1 standard.  The gunicorn server should set
    the flag, but this feature has not been implemented.
    """
    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == "chunked":
        request.environ["wsgi.input_terminated"] = True
