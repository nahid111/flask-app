import os

SECRET_KEY = os.getenv('SECRET_KEY')

# ===================================================================
#                       File upload directories
# ===================================================================
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
UPOLADS_FOLDER = os.path.join(APP_ROOT, "uploads/")
if not os.path.isdir(UPOLADS_FOLDER):
    os.mkdir(UPOLADS_FOLDER)

# ===================================================================
#                       Database credentials
# ===================================================================
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# SQLALCHEMY_DATABASE_URI=mysql+pymysql://DB_USERNAME:DB_PASSWORD:@DB_HOST/DB_NAME
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
CSRF_ENABLED = os.getenv('CSRF_ENABLED')

# ===================================================================
#                       Flask-Mail settings
# ===================================================================
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
