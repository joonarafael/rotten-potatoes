from app import app
from flask import redirect, render_template, request, session, flash
from utils.flash import clear_session_flashes
from sql.genres import get_all_genres
from sql.movies import add_movie, get_all_movies, get_movie_by_id, rate_movie
from datetime import datetime


@app.route("/movies", methods=["GET"])
def page_movies():
    movies = get_all_movies()

    if not movies["success"]:
        print(movies["error"])

        return render_template("movies.html", movies=[])
    
    user_id = session["user_id"] if "user_id" in session else None

    for movie in movies["data"]:
        rated = False

        if user_id:
            for review in movie["reviews"]:
                if review["user_id"] == user_id:
                    rated = True
                    break

        movie["rated"] = rated
    
    return render_template("movies.html", movies=movies["data"])

@app.route("/movies/<id>", methods=["GET"])
def page_movie(id: str):
    clear_session_flashes()

    if not id or not isinstance(id, str):
        flash("Given ID was invalid.", 'error')
        return redirect("/movies")

    movie = get_movie_by_id(id)

    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])

    user_id = session["user_id"] if "user_id" in session else None
    rated = False

    if user_id:
        for review in movie["data"]["reviews"]:
            if review["user_id"] == user_id:
                rated = True
                break

    movie["data"]["rated"] = rated    

    return render_template("movie.html", movie=movie["data"])

@app.route("/movies/add", methods=["GET"])
def page_add_movie():
    genres = get_all_genres()

    if not genres["success"]:
        print(genres["error"])

        return render_template("error.html", error=genres["error"])
    
    return render_template("movies.add.html", genres=genres["data"])


@app.route("/movies/rate/<id>", methods=["GET"])
def page_rate_movie(id: str):
    if "username" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")

    movie = get_movie_by_id(id)

    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])
    
    return render_template("movies.rate.html", movie=movie["data"])


@app.route("/api/movies", methods=["POST"])
def api_post_movie():
    clear_session_flashes()
    # auth
    if "username" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")
    
    if session["csrf_token"] != request.form["csrf_token"]:
        flash("CSRF token mismatch. You may have to login again.", 'error')
        return redirect("/movies/add")

    # actual logic
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
        
        db_result = add_movie(title, genre, description, year_as_int, session["user_id"])

        if not db_result["success"]:
            if "UniqueViolation" in db_result["error"]:
                flash("Movie adding failed. Movie named '{}' already exists.".format(title), 'error')

            else:
                flash("Movie adding failed. Please try again.", 'error')
            
            return redirect("/movies/add")

        flash("Movie adding successful!", 'success')
        return redirect("/movies")

    except Exception as e:
        print(e)
        flash("Movie adding failed. {}".format(e), 'error')
        return redirect("/movies/add")


@app.route("/api/movies/rate/<id>", methods=["POST"])
def api_rate_movie(id: str):
    clear_session_flashes()

    if not id or not isinstance(id, str):
        flash("Given ID was invalid.", 'error')
        return redirect("/movies")

    # auth
    if "username" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")
    
    if session["csrf_token"] != request.form["csrf_token"]:
        flash("CSRF token mismatch. You may have to login again.", 'error')
        return redirect("/movies/add")
    
    movie = get_movie_by_id(id)

    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])

    # actual logic
    try:
        rating = request.form["rating"]
        comment = request.form["comment"]

        # sanity checks
        if not rating or not comment:
            flash("Rating and comment are required.", 'error')
            return redirect("/movies/rate/{}".format(id))
        
        if not isinstance(rating, str) or not isinstance(comment, str):
            flash("Rating and comment must be of type string.", 'error')
            return redirect("/movies/rate/{}".format(id))

        rating_as_int = int(rating)

        if rating_as_int < 1 or rating_as_int > 10:
            flash("Rating must be equal to or greater than 1 and equal to or less than 10.", 'error')
            return redirect("/movies/rate/{}".format(id))
        
        if len(comment) < 4 or len(comment) > 1024:
            flash("Title must be between 4 and 1024 characters.", 'error')
            return redirect("/movies/rate/{}".format(id))
        
        db_result = rate_movie(id, rating_as_int, comment, session["user_id"])

        if not db_result["success"]:
            if "has already" in db_result["error"]:
                flash("Movie rating failed. You have already given a rating!", 'error')

            else:
                flash("Movie rating failed. Please try again.", 'error')
            
            return redirect("/movies/rate/{}".format(id))

        flash("Movie rating successful!", 'success')
        return redirect("/movies")

    except Exception as e:
        print(e)
        flash("Movie rating failed. {}".format(e), 'error')
        return redirect("/movies/rate/{}".format(id))

