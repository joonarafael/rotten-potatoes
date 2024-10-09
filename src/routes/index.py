from app import app
from flask import render_template, session
from sql.movies import get_all_movies


@app.route("/", methods=["GET"])
def page_index():
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
