from app import app
from flask import redirect, render_template, request, session, flash
from sql.users import get_user_by_id
from utils.flash import clear_session_flashes
from utils.validate_movie_details import validate_movie_details
from sql.genres import get_all_genres
from sql.movies import add_movie, get_all_movies, get_movie_by_id, rate_movie, delete_movie_by_id, get_rating_by_id, delete_rating_by_id, edit_movie_by_id
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
    if not id or not isinstance(id, str):
        flash("Given ID was invalid.", 'error')
        return redirect("/movies")

    movie = get_movie_by_id(id)

    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])
    
    created_by = get_user_by_id(movie["data"]["created_by"])

    if not created_by["success"]:
        movie["data"]["created_by_user"] = "N/A"
    else:
        movie["data"]["created_by_user"] = created_by["data"]["username"]

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

@app.route("/movies/edit/<id>", methods=["GET"])
def page_edit_movie(id: str):
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")
    
    user = get_user_by_id(session["user_id"])

    if not user["success"]:
        print(user["error"])

        return render_template("error.html", error=user["error"])
    
    if user["data"]["is_admin"] == False:
        flash("You are not allowed to edit movies.", 'error')
        return redirect("/movies/{}".format(id))

    movie = get_movie_by_id(id)

    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])
    
    genres = get_all_genres()

    if not genres["success"]:
        print(genres["error"])

        return render_template("error.html", error=genres["error"])
    
    print(movie["data"])
    
    return render_template("movies.edit.html", movie=movie["data"], genres=genres["data"])


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

        validated = validate_movie_details(title, genre, description, year)

        if validated:
            db_result = add_movie(title, genre, description, int(year), session["user_id"])

            if not db_result["success"]:
                if "UniqueViolation" in db_result["error"]:
                    flash("Movie adding failed. Movie named '{}' already exists.".format(title), 'error')

                else:
                    flash("Movie adding failed. Please try again.", 'error')
                
                return redirect("/movies/add")

            flash("Movie adding successful!", 'success')
            return redirect("/movies")
        
        return redirect("/movies/add")

    except Exception as e:
        print(e)
        flash("Movie adding failed. {}".format(e), 'error')
        return redirect("/movies/add")


@app.route("/api/movies/<id>", methods=["POST"])
def api_delete_movie(id: str):
    clear_session_flashes()
    # auth
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")
    
    if session["csrf_token"] != request.form["csrf_token"]:
        flash("CSRF token mismatch. You may have to login again.", 'error')
        return redirect("/movies/{}".format(id))

    user = get_user_by_id(session["user_id"])
    movie = get_movie_by_id(id)

    if not user["success"]:
        print(user["error"])

        return render_template("error.html", error=user["error"])
    
    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])
    
    # check for admin / owner
    if not user["data"]["is_admin"]:
        if session["user_id"] != movie["data"]["created_by"]:
            flash("You are not allowed to delete this movie.", 'error')
            return redirect("/movies/{}".format(id))

    # actual logic
    try:
        db_result = delete_movie_by_id(id, user["data"]["is_admin"])

        if not db_result["success"]:
            flash(db_result["error"], 'error')
            
            return redirect("/movies/{}".format(id))

        flash("Movie deletion successful!", 'success')
        return redirect("/movies")

    except Exception as e:
        print(e)
        flash("Movie deletion failed. {}".format(e), 'error')
        return redirect("/movies/{}".format(id))


@app.route("/api/movies/edit/<id>", methods=["PUT", "POST"])
def api_edit_movie(id: str):
    clear_session_flashes()
    # auth
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")
    
    if session["csrf_token"] != request.form["csrf_token"]:
        flash("CSRF token mismatch. You may have to login again.", 'error')
        return redirect("/movies/{}".format(id))

    user = get_user_by_id(session["user_id"])
    movie = get_movie_by_id(id)

    if not user["success"]:
        print(user["error"])

        return render_template("error.html", error=user["error"])
    
    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])
    
    # check for admin
    if not user["data"]["is_admin"]:
        flash("You are not allowed to edit movie details.", 'error')
        return redirect("/movies/{}".format(id))

    # actual logic
    try:
        title = request.form["title"]
        genre = request.form["genre"]
        description = request.form["description"]
        year = request.form["year"]

        validated = validate_movie_details(title, genre, description, year)

        if validated:
            db_result = edit_movie_by_id(id, title, genre, description, int(year))

            if not db_result["success"]:
                if "UniqueViolation" in db_result["error"]:
                    flash("Movie editing failed. Movie named '{}' already exists.".format(title), 'error')

                else:
                    flash("Movie editing failed. Please try again.", 'error')
                
                return redirect("/movies/edit/{}".format(id))

            flash("Movie editing successful!", 'success')
            return redirect("/movies")
        
        return redirect("/movies/edit/{}".format(id))
    
    except Exception as e:
        print(e)
        flash("Movie editing failed. {}".format(e), 'error')
        return redirect("/movies/edit/{}".format(id))


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

@app.route("/api/movies/rate/delete/<id>", methods=["POST"])
def api_delete_rating(id: str):
    clear_session_flashes()
    # auth
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")
    
    if session["csrf_token"] != request.form["csrf_token"]:
        flash("CSRF token mismatch. You may have to login again.", 'error')
        return redirect("/movies/{}".format(id))

    user = get_user_by_id(session["user_id"])
    rating = get_rating_by_id(id)

    if not user["success"]:
        print(user["error"])

        return render_template("error.html", error=user["error"])
    
    if not rating["success"]:
        print(rating["error"])

        return render_template("error.html", error=rating["error"])
    
    # check for ownership
    # admin can delete any rating
    if not user["data"]["is_admin"]:
        if session["user_id"] != rating["data"]["user_id"]:
            flash("You are not allowed to delete this rating!", 'error')
            return redirect("/movies/{}".format(id))

    # actual logic
    try:
        db_result = delete_rating_by_id(id, user["data"]["is_admin"])

        if not db_result["success"]:
            flash(db_result["error"], 'error')
            
            return redirect("/movies/{}".format(id))

        flash("Rating deletion successful!", 'success')
        return redirect("/movies")

    except Exception as e:
        print(e)
        flash("Rating deletion failed. {}".format(e), 'error')
        return redirect("/movies/{}".format(id))