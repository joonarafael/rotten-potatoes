
"""Route handlers for authentication-related routes."""

# pylint: disable=import-error
# pylint: disable=broad-exception-caught


from typing import Callable
from flask import redirect, render_template, request, flash
from app import app
from sql.users import register, login, logout


@app.route("/auth/login", methods=["GET"])
def page_login() -> Callable:
    """GET method for the Login page.

    Returns:
        render_template: Returns the HTML page called "auth.login.html".
    """
    return render_template("auth.login.html")


@app.route("/auth/register", methods=["GET"])
def page_register() -> Callable:
    """GET method for the Register page.

    Returns:
        render_template: Returns the HTML page called "auth.register.html".
    """
    return render_template("auth.register.html")


@app.route("/auth/logout", methods=["GET"])
def api_logout() -> Callable:
    """GET method to logout the user.

    Returns:
        redirect: Redirects back home.
    """
    logout()
    return redirect("/")


@app.route("/api/auth/login", methods=["POST"])
def api_login() -> Callable:
    """API POST method for a user to log in.

    Returns:
        redirect: Redirects to the user's profile page if successful,
        otherwise back to the login page with a proper error message.
    """
    try:
        username = request.form["username"]
        password = request.form["password"]
    except Exception as e:
        print(e)
        flash("Username and password are required.", 'error')
        return redirect("/auth/register")

    try:
        # sanity checks for user input
        if not username or not password:
            flash("Username and password are required.", 'error')
            return redirect("/auth/login")

        if not isinstance(username, str) or not isinstance(password, str):
            flash("Username and password must be of type string.", 'error')
            return redirect("/auth/login")

        if len(username) > 64:
            flash("Username must be at most 64 characters.", 'error')
            return redirect("/auth/login")

        if len(password) > 64:
            flash("Password must be at most 64 characters.", 'error')
            return redirect("/auth/login")

        db_result = login(username, password)

        if not db_result["success"]:
            flash("Incorrect username or password!", 'error')
            return redirect("/auth/login")

        flash("Login successful!", 'success')
        return redirect("/profile")

    except Exception as e:
        print(e)
        flash(f"Login failed. {e}", 'error')
        return redirect("/auth/login")


@app.route("/api/auth/register", methods=["POST"])
def api_register() -> Callable:
    """API POST method for a new user to register.

    Returns:
        redirect: Redirects to the login page if successful,
        otherwise stays on the register page with an error message.
    """
    try:
        username = request.form["username"]
        password = request.form["password"]
    except Exception as e:
        print(e)
        flash("Username and password are required.", 'error')
        return redirect("/auth/register")

    try:
        # sanity checks for user input
        if not username or not password:
            flash("Username and password are required.", 'error')
            return redirect("/auth/register")

        if not isinstance(username, str) or not isinstance(password, str):
            flash("Username and password must be of type string.", 'error')
            return redirect("/auth/register")

        if len(username) < 4 or len(username) > 64:
            flash("Username must be between 4 and 64 characters.", 'error')
            return redirect("/auth/register")

        if len(password) < 4 or len(password) > 64:
            flash("Password must be between 4 and 64 characters.", 'error')
            return redirect("/auth/register")

        db_result = register(username, password)

        if not db_result["success"]:
            if "UniqueViolation" in db_result["error"]:
                flash("Registration failed. Username already exists.", 'error')

            else:
                flash("Registration failed. Please try again.", 'error')

            return redirect("/auth/register")

        flash("Registration successful!", 'success')
        return redirect("/auth/login")

    except Exception as e:
        print(e)
        flash(f"Registration failed. {e}", 'error')
        return redirect("/auth/register")
