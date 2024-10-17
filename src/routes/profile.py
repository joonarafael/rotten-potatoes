"""Route handler for the profile route."""

# pylint: disable=import-error
# pylint: disable=broad-exception-caught


from typing import Callable
from flask import redirect, render_template, session, flash
from app import app
from sql.users import get_user_by_id


@app.route("/profile", methods=["GET"])
def page_profile() -> Callable:
    """GET method for the Profile page.

    Returns:
        redirect | render_template: Redirects to login if unauthenticated,
        otherwise renders the profile page.
    """
    # check for user ID in session details
    if "user_id" not in session or not isinstance(session["user_id"], str):
        flash("You must be logged in to view this page.", 'error')
        return redirect("/auth/login")

    user_details = get_user_by_id(session["user_id"])

    if not user_details["success"]:
        print(user_details["error"])

        return render_template("error.html", error=user_details["error"])

    return render_template("profile.html", user_details=user_details["data"])
