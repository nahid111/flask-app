import os
from dotenv import load_dotenv
from flask import Flask
from app_extensions import db, ma, mail
from controllers.auth import auth_module

# load dotenv in the base root
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


# ===================================================================
#                        Handle App Errors
# ===================================================================
# @app.errorhandler(Exception)
# def handle_error(error):
#     # print in red
#     print('\x1b[91m' + str(error) + '\x1b[0m')
#     # message = [str(x) for x in error.args]
#     return {'success': False, 'error': "internal server error"}, 500


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(auth_module, url_prefix='/api/v1/auth')

    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)

    return None
