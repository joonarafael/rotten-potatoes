from app import app
from flask import redirect, render_template, request, session


@app.route("/movies", methods=["GET"])
def page_movies():
    return render_template("movies.html")


@app.route("/movies/add", methods=["GET"])
def page_add_movie():
    return render_template("movies.add.html")


@app.route("/api/movie", methods=["POST"])
def api_post_movie():
    return

    # TODO: Implement adding movies API


@app.route("/api/movie/<int:id>", methods=["GET", "PUT", "DELETE"])
def api_get_put_delete_movie(id):
    return

    # TODO: Implement getting, updating and deleting movies
