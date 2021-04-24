from flask_script import Manager, Command, Option
from flask_migrate import Migrate, MigrateCommand
from app import app, db, dummy_data_creator

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def dummy(size="small"):
    dummy_data_creator.add_dummy_data(size)


if __name__ == '__main__':
    manager.run()
