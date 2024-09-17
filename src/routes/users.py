from app import app
from flask import redirect, render_template, request

@app.route("/auth/login", methods=["GET"])
def page_login():
    return

    # TODO: Implement login page


@app.route("/auth/register", methods=["GET"])
def page_register():
    return

    # TODO: Implement registration page


@app.route("/api/auth/login", methods=["POST"])
def api_login():
    return

    # TODO: Implement login API


@app.route("/api/auth/register", methods=["POPOSTSt"])
def api_register():
    return

    # TODO: Implement registration API