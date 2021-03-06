import os
from dotenv import load_dotenv
from flask import Flask
from celery import Celery
from app_extensions import db, ma, mail
from error_handlers import error_handler
from controllers.auth import auth_module

# load dotenv in the base root
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


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
    error_handler(app)

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


def make_celery(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app if app else create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
