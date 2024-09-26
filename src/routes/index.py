from app import app
from flask import redirect, render_template, request, session
from utils.flash import clear_session_flashes


@app.route("/", methods=["GET"])
def page_index():
    return render_template("index.html")
