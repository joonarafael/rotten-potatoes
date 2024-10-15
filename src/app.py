"""Main Flask app entrypoint."""

# pylint: disable=wrong-import-position
# pylint: disable=unused-import


from os import getenv
from flask import Flask


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")


from routes import profile
from routes import search
from routes import index
from routes import users
from routes import movies