import os
from dotenv import load_dotenv
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail

''' load dotenv in the base root '''
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


# ===================================================================
#                          instantiate app
# ===================================================================
app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)


# ===================================================================
#                        Handle App Errors
# ===================================================================
@app.errorhandler(Exception)
def handle_error(error):
    print('\x1b[91m' + str(error) + '\x1b[0m')
    # message = [str(x) for x in error.args]
    return {'success': False, 'error': 'internal server error'}, 500


# ===================================================================
#                 import & register View blueprints
# ===================================================================
from controllers.auth import auth_module
app.register_blueprint(auth_module, url_prefix='/api/v1/auth')


