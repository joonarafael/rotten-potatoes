from app import app
from flask import redirect, render_template, request, flash, session
from sql.users import register, login, logout
from utils.flash import clear_session_flashes

@app.route("/auth/login", methods=["GET"])
def page_login():
    return render_template("auth.login.html")


@app.route("/auth/register", methods=["GET"])
def page_register():
    return render_template("auth.register.html")


@app.route("/auth/logout", methods=["GET"])
def api_logout():
    logout()
    return redirect("/auth/login")


@app.route("/api/auth/login", methods=["POST"])
def api_login():
    clear_session_flashes()
    try:
        username = request.form["username"]
        password = request.form["password"]

        # sanity checks
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
        flash("Login failed. {}".format(e), 'error')
        return redirect("/auth/login")


@app.route("/api/auth/register", methods=["POST"])
def api_register():
    clear_session_flashes()
    try:
        username = request.form["username"]
        password = request.form["password"]

        # sanity checks
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
        flash("Registration failed. {}".format(e), 'error')
        return redirect("/auth/register")
