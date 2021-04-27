from flask import Flask
from config import Config
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
CORS(app)

from . import routes
from .dummy_data_creator import *


# Adds dummy data to the database
@click.command(name='dummy-data')
@click.argument('size')
@with_appcontext
def dummy_data(size):
    """Adds dummy data to the database"""
    add_dummy_data(size)


app.cli.add_command(dummy_data)


from .cron_jobs import *