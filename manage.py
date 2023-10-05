import os
# from flask_script import Manager
import alembic
from flask_migrate import Migrate, MigrateCommand
from flask import current_app as app
from database import database

migrate = Migrate(app, database.db)
# manager = Manager(app)
#
# manager.add_command("db", MigrateCommand)

# if __name__ == "__main__":
#     manager.run()
