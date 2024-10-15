"""Module for the DB setup."""


from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)
