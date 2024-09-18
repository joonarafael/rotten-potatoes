from app import app
from flask import redirect, render_template, request, flash
from sql.users import register, logout

@app.route("/auth/login", methods=["GET"])
def page_login():
    return render_template("auth.login.html")


@app.route("/auth/register", methods=["GET"])
def page_register():
    return render_template("auth.register.html")


@app.route("/api/auth/login", methods=["POST"])
def api_login():
    try:
        username = request.form["username"]
        password = request.form["password"]

        print(f"Username: {username}, Password: {password}")

        return {"message": "Login successful!"}

    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/api/auth/register", methods=["POST"])
def api_register():
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
            flash("Registration failed. Please try again.", 'error')
            return redirect("/auth/register")

        flash("Registration successful!", 'success')
        return redirect("/auth/login")

    except Exception as e:
        print(e)

        flash("Registration failed. Please try again.", 'error')
        return redirect("/auth/register")

@app.route("/api/auth/logout", methods=["HEAD"])
def api_logout():
    logout()

    redirect("/")