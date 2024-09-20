from app import app
from flask import redirect, render_template, request, session, flash
from sql.genres import get_all_genres
from datetime import datetime


@app.route("/movies", methods=["GET"])
def page_movies():
    return render_template("movies.html")


@app.route("/movies/add", methods=["GET"])
def page_add_movie():
    genres = get_all_genres()

    if not genres["success"]:
        print(genres["error"])

        return render_template("error.html", error=genres["error"])
    
    return render_template("movies.add.html", genres=genres["data"])


@app.route("/api/movies", methods=["POST"])
def api_post_movie():
    try:
        title = request.form["title"]
        genre = request.form["genre"]
        description = request.form["description"]
        year = request.form["year"]

        genres = get_all_genres()

        if not genres["success"]:
            print(genres["error"])

            return render_template("error.html", error=genres["error"])
        
        genre_ids = [genre["id"] for genre in genres["data"]]

        # sanity checks
        if not title or not genre or not description or not year:
            flash("Title, genre, description and year are required.", 'error')
            return redirect("/movies/add")
        
        if not isinstance(title, str) or not isinstance(genre, str) or not isinstance(description, str) or not isinstance(year, str):
            flash("Title, genre, description and year must be of type string.", 'error')
            return redirect("/movies/add")
        
        if len(title) < 4 or len(title) > 64:
            flash("Title must be between 4 and 64 characters.", 'error')
            return redirect("/movies/add")
        
        if genre not in genre_ids:
            flash("Unknown genre.", 'error')
            return redirect("/movies/add")
        
        year_as_int = int(year)
        
        if year_as_int < 1900 or year_as_int > datetime.now().year:
            flash("Year must be between greater than 1900 and equal to or less than {}.".format(datetime.now().year), 'error')
            return redirect("/movies/add")

        flash("Movie adding successful!", 'success')
        return redirect("/movies")


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


@app.route("/api/movies/<int:id>", methods=["GET", "PUT", "DELETE"])
def api_get_put_delete_movie(id):
    return

    # TODO: Implement getting, updating and deleting movies
