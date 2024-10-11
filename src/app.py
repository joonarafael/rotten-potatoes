from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

from routes import profile
from routes import search
from routes import index
from routes import users
from routes import movies