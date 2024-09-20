from app import app
from flask import redirect, render_template, request, session
from sql.genres import get_all_genres


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


@app.route("/api/movie", methods=["POST"])
def api_post_movie():
    return

    # TODO: Implement adding movies API


@app.route("/api/movie/<int:id>", methods=["GET", "PUT", "DELETE"])
def api_get_put_delete_movie(id):
    return

    # TODO: Implement getting, updating and deleting movies
