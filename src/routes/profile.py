from app import app
from flask import redirect, render_template, request, session, flash


@app.route("/profile", methods=["GET"])
def page_profile():
    return render_template("profile.html")