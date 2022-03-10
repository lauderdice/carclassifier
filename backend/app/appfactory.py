import os
import uuid

import flask
from flask import Flask

from app.common.config import setup_environment, setup_flask_logging


def create_application() -> flask.app.Flask:
    from app.api.routers.webapp_routers import webapp
    app = Flask(__name__)
    app.secret_key = str(uuid.uuid4())
    app.url_map.strict_slashes = False
    setup_environment(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "common/env_files/.common_env"))
    app = setup_flask_logging(app)
    app.register_blueprint(webapp)
    # app.register_blueprint(api)
    return app

application = create_application()