from app import app
from flask import redirect, render_template, request, session, flash
from utils.flash import clear_session_flashes
from sql.users import get_user_by_id


@app.route("/profile", methods=["GET"])
def page_profile():
    if "user_id" not in session or not isinstance(session["user_id"], str):
        flash("You must be logged in to view this page.", 'error')
        return redirect("/auth/login")

    user_details = get_user_by_id(session["user_id"])

    if not user_details["success"]:
        print(user_details["error"])

        return render_template("error.html", error=user_details["error"])

    return render_template("profile.html", user_details=user_details["data"])