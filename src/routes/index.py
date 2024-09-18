from app import app
from flask import redirect, render_template, request


@app.route("/", methods=["GET"])
def page_index():
    return render_template("index.html")
