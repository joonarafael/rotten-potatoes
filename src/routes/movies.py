"""Route handlers for all movie-related routes."""

# pylint: disable=import-error
# pylint: disable=broad-exception-caught

# pylint: disable=redefined-builtin
# i want to use `id` as variable name but pylint ain't having it


from flask import redirect, render_template, request, session, flash
from app import app
from utils.validate_movie_details import validate_movie_details
from sql.genres import get_all_genres
from sql.movies import add_movie, get_movie_by_id, rate_movie, delete_movie_by_id, get_rating_by_id, delete_rating_by_id, edit_movie_by_id
from sql.users import get_user_by_id


@app.route("/movies", methods=["GET"])
def page_movies() -> redirect:
    """GET method for the Movies page.

    Returns:
        redirect: Redirects back to the home page.
    """
    return redirect("/")


@app.route("/movies/<id>", methods=["GET"])
def page_movie(id: str) -> render_template:
    """GET method for the Movie page.

    Args:
        id (str): Movie ID to query the database with.

    Returns:
        render_template: Returns the HTML page called "movie.html" with
        the movie details (if only found).
    """
    if not id or not isinstance(id, str):
        return render_template(
            "error.html",
            error="Given movie ID was invalid.")

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
def page_add_movie() -> redirect | render_template:
    """GET method for the Add Movie page.

    Returns:
        redirect | render_template: Returns the HTML page
        called"movies.add.html" with a form to add a new movie.
    """
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")

    genres = get_all_genres()

    if not genres["success"]:
        print(genres["error"])

        return render_template("error.html", error=genres["error"])

    return render_template("movies.add.html", genres=genres["data"])


@app.route("/movies/rate/<id>", methods=["GET"])
def page_rate_movie(id: str) -> redirect | render_template:
    """GET method for the Rate Movie page.

    Args:
        id (str): ID of the movie to rate.

    Returns:
        redirect | render_template: Returns the HTML page
        called "movies.rate.html" with a form to rate a movie.
    """
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")

    user = get_user_by_id(session["user_id"])

    if not user["success"]:
        print(user["error"])

        return render_template("error.html", error=user["error"])

    # proper auth for csrf will be done in the API
    # HTML page is be returned if some session data is found

    movie = get_movie_by_id(id)

    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])

    return render_template("movies.rate.html", movie=movie["data"])


@app.route("/movies/edit/<id>", methods=["GET"])
def page_edit_movie(id: str) -> redirect | render_template:
    """GET method for the Edit Movie page.

    Args:
        id (str): ID of the movie to edit.

    Returns:
        redirect | render_template: Returns the HTML page
        called "movies.edit.html" with a form to edit a movie.
    """
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")

    user = get_user_by_id(session["user_id"])

    if not user["success"]:
        print(user["error"])

        return render_template("error.html", error=user["error"])

    if not user["data"]["is_admin"]:
        flash("You are not allowed to edit movies.", 'error')
        return redirect(f"/movies/{id}")

    # proper auth for csrf will be done in the API
    # HTML page is be returned if some session data is found

    movie = get_movie_by_id(id)

    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])

    genres = get_all_genres()

    if not genres["success"]:
        print(genres["error"])

        return render_template("error.html", error=genres["error"])

    return render_template(
        "movies.edit.html",
        movie=movie["data"],
        genres=genres["data"])


@app.route("/api/movies", methods=["POST"])
def api_post_movie() -> redirect:
    """API POST method for a logged-in user to add a new movie to the database.

    Returns:
        redirect: Redirects to appropriate pages
        based on the success of the movie addition.
    """
    # auth with csrf
    if "username" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")

    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            flash("CSRF token mismatch. You may have to login again.", 'error')
            return redirect("/movies/add")
    except Exception as e:
        print(e)
        flash("Unauthorized. Log in again.", 'error')
        return redirect("/auth/login")

    try:
        title = request.form["title"]
        genre = request.form["genre"]
        description = request.form["description"]
        year = request.form["year"]
    except Exception as _:
        flash(
            "Movie adding failed. Title, genre, description or year was missing.",
            'error')
        return redirect("/movies/add")

    try:
        validated = validate_movie_details(title, genre, description, year)

        if validated:
            db_result = add_movie(
                title,
                genre,
                description,
                int(year),
                session["user_id"])

            if not db_result["success"]:
                if "UniqueViolation" in db_result["error"]:
                    flash(
                        f"Movie adding failed. Movie named '{title}' already exists.",
                        'error')

                else:
                    flash("Movie adding failed. Please try again.", 'error')

                return redirect("/movies/add")

            flash("Movie adding successful!", 'success')
            return redirect("/movies")

        return redirect("/movies/add")

    except Exception as e:
        print(e)
        flash(f"Movie adding failed. {e}", 'error')
        return redirect("/movies/add")


@app.route("/api/movies/<id>", methods=["POST"])
def api_delete_movie(id: str) -> redirect:
    """API POST method for a user to delete their movie from the database.
    Admins can delete any movie.

    Args:
        id (str): ID of the movie to delete.

    Returns:
        redirect: Redirects to appropriate pages
        based on the success of the movie deletion.
    """
    # auth with csrf
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")

    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            flash("CSRF token mismatch. You may have to login again.", 'error')
            return redirect("/movies/add")
    except Exception as _:
        flash("Unauthorized. Log in again.", 'error')
        return redirect("/auth/login")

    # get details and check for true user
    # check both entities actually exist in the database
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
            return redirect(f"/movies/{id}")

    try:
        db_result = delete_movie_by_id(id, user["data"]["is_admin"])

        if not db_result["success"]:
            flash(db_result["error"], 'error')

            return redirect(f"/movies/{id}")

        flash("Movie deletion successful!", 'success')
        return redirect("/movies")

    except Exception as e:
        print(e)
        flash(f"Movie deletion failed. {e}", 'error')
        return redirect(f"/movies/{id}")


@app.route("/api/movies/edit/<id>", methods=["PUT", "POST"])
def api_edit_movie(id: str) -> redirect:
    """API PUT & POST method for an admin to edit their movie details.

    Args:
        id (str): ID of the movie to edit.§

    Returns:
        redirect: Redirects to appropriate pages
        based on the success of the movie editing.
    """
    # auth with csrf
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")

    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            flash("CSRF token mismatch. You may have to login again.", 'error')
            return redirect("/movies/add")
    except Exception as e:
        print(e)
        flash("Unauthorized. Log in again.", 'error')
        return redirect("/auth/login")

    # get details and check for 'true' user from db
    # verify the movie exists in db
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
        return redirect(f"/movies/{id}")

    try:
        title = request.form["title"]
        genre = request.form["genre"]
        description = request.form["description"]
        year = request.form["year"]
    except Exception as _:
        flash(
            "Movie editing failed. Title, genre, description or error was missing.",
            'error')
        return redirect(f"/movies/edit/{id}")

    try:
        validated = validate_movie_details(title, genre, description, year)

        if validated:
            db_result = edit_movie_by_id(
                id, title, genre, description, int(year))

            if not db_result["success"]:
                if "UniqueViolation" in db_result["error"]:
                    flash(
                        f"Movie editing failed. Movie named '{title}' already exists.",
                        'error')

                else:
                    flash("Movie editing failed. Please try again.", 'error')

                return redirect(f"/movies/edit/{id}")

            flash("Movie editing successful!", 'success')
            return redirect(f"/movies/{id}")

        return redirect(f"/movies/edit/{id}")

    except Exception as e:
        print(e)
        flash(f"Movie editing failed. {e}", 'error')
        return redirect(f"/movies/edit/{id}")


@app.route("/api/movies/rate/<id>", methods=["POST"])
def api_rate_movie(id: str) -> redirect:
    """API POST method for a user to send their rating.

    Args:
        id (str): ID of the movie to rate.

    Returns:
        redirect: Redirects to appropriate pages
        based on the success of the movie rating.
    """
    if not id or not isinstance(id, str):
        flash("Given ID was invalid.", 'error')
        return redirect("/movies")

    # auth with csrf
    if "username" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")

    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            flash("CSRF token mismatch. You may have to login again.", 'error')
            return redirect("/movies/add")
    except Exception as e:
        print(e)
        flash("Unauthorized. Log in again.", 'error')
        return redirect("/auth/login")

    # get movie details & check it exists
    movie = get_movie_by_id(id)

    if not movie["success"]:
        print(movie["error"])

        return render_template("error.html", error=movie["error"])

    try:
        rating = request.form["rating"]
        comment = request.form["comment"]
    except Exception as _:
        flash("Movie rating failed. Stars or comment was missing.", 'error')
        return redirect(f"/movies/rate/{id}")

    try:
        # quick sanity checks for user input
        if not rating or not comment:
            flash("Rating and comment are required.", 'error')
            return redirect(f"/movies/rate/{id}")

        if not isinstance(rating, str) or not isinstance(comment, str):
            flash("Rating and comment must be of type string.", 'error')
            return redirect(f"/movies/rate/{id}")

        rating_as_int = int(rating)

        if rating_as_int < 1 or rating_as_int > 10:
            flash(
                "Rating must be equal to or greater than 1 and equal to or less than 10.",
                'error')
            return redirect(f"/movies/rate/{id}")

        if len(comment) < 4 or len(comment) > 1024:
            flash("Comment must be between 4 and 1024 characters.", 'error')
            return redirect(f"/movies/rate/{id}")

        db_result = rate_movie(id, rating_as_int, comment, session["user_id"])

        if not db_result["success"]:
            if "has already" in db_result["error"]:
                flash(
                    "Movie rating failed. You have already given a rating!",
                    'error')

            else:
                flash("Movie rating failed. Please try again.", 'error')

            return redirect(f"/movies/rate/{id}")

        flash("Movie rating successful!", 'success')
        return redirect(f"/movies/{id}")

    except Exception as e:
        print(e)
        flash(f"Movie rating failed. {e}", 'error')
        return redirect(f"/movies/rate/{id}")


@app.route("/api/movies/rate/delete/<id>", methods=["POST"])
def api_delete_rating(id: str) -> redirect | render_template:
    """API POST method for a user to delete their rating from the database.

    Args:
        id (str): ID of the rating to delete.

    Returns:
        redirect | render_template: Redirects to appropriate pages
        based on the success of the rating deletion.
        Error case renders the error template.
    """
    # auth with csrf
    if "user_id" not in session:
        flash("No user logged in.", 'error')
        return redirect("/auth/login")

    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            flash("CSRF token mismatch. You may have to login again.", 'error')
            return redirect("/movies/add")
    except Exception as e:
        print(e)
        flash("Unauthorized. Log in again.", 'error')
        return redirect("/auth/login")

    # get details & check all entities exist in db
    user = get_user_by_id(session["user_id"])
    rating = get_rating_by_id(id)

    if not user["success"]:
        print(user["error"])

        return render_template("error.html", error=user["error"])

    if not rating["success"]:
        print(rating["error"])

        return render_template("error.html", error=rating["error"])

    # check for ownership / admin
    # note that admin can delete any rating
    if not user["data"]["is_admin"]:
        if session["user_id"] != rating["data"]["user_id"]:
            flash("You are not allowed to delete this rating!", 'error')
            return redirect("/movies")

    try:
        db_result = delete_rating_by_id(id, user["data"]["is_admin"])

        if not db_result["success"]:
            flash(db_result["error"], 'error')

            return redirect("/movies")

        flash("Rating deletion successful!", 'success')
        return redirect("/movies")

    except Exception as e:
        print(e)
        flash(f"Rating deletion failed. {e}", 'error')
        return redirect("/movies")
