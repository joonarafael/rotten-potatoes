from flask import Flask
from flask import render_template
from flask import Flask
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)


@app.route("/")
def index():
    try:
        result = db.session.execute(text("SELECT * FROM users"))
        print(result.fetchall())

    except Exception as e:
        print(e)

    return render_template("index.html")

