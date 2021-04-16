from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
from .dummy_data_creator import *


# Adds dummy data to the database
@click.command(name='dummy-data')
@with_appcontext
def dummy_data():
    add_dummy_data()


app.cli.add_command(dummy_data)
