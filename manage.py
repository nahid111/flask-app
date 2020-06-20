from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import *
from app import create_app
from app_extensions import db

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()


# =======================================================================================
#           creating/updating tables with flask migrate
# =======================================================================================

''' run the following command to create the migration folder (for the 1st time only) '''
# $ python3 manage.py db init

''' run the following command to create the migration file '''
# $ python3 manage.py db migrate

''' run the following command to apply the migrations '''
# $ python3 manage.py db upgrade







