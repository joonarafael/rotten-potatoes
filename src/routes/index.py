"""Route handler for the Index page (e.g. Movies page / Movie list page)"""

# pylint: disable=wrong-import-position
# pylint: disable=unused-import
# pylint: disable=import-error


from flask import render_template, session
from app import app
from sql.movies import get_all_movies


@app.route("/", methods=["GET"])
def page_index() -> render_template:
    """GET method for the Index page.

    Returns:
        render_template: HTML page called "movies.html" with the appropriate movies data, if any.
    """
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
