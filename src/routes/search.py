from app import app
from flask import redirect, render_template, request, flash
from sql.genres import get_all_genres
from sql.movies import get_all_movies, get_movie_by_id


@app.route("/search", methods=["GET"])
def page_search():
    genres = get_all_genres()

    if not genres["success"]:
        print(genres["error"])

        return render_template("error.html", error=genres["error"])

    return render_template("search.html", genres=genres["data"])


@app.route("/search/results/", methods=["GET"])
def page_search_no_results():
    return render_template("search.no.results.html")


@app.route("/search/results/<results>", methods=["GET"])
def page_search_results(results: str):
    if not results or not isinstance(results, str):
        return render_template("error.html", error="Invalid URL!")

    try:
        movie_ids = results.split(",")
        movies = []

        for movie_id in movie_ids:
            movie = get_movie_by_id(movie_id)

            if not movie["success"]:
                print(movie["error"])
                return render_template("error.html", error=movie["error"])

            movies.append(movie["data"])

        return render_template("search.results.html", movies=movies)

    except Exception as e:
        print(e)
        return render_template(
            "error.html",
            error="An error occurred while fetching search results.")


@app.route("/api/search", methods=["POST"])
def api_search_results():
    try:
        title = request.form["title"]
    except KeyError:
        title = None

    try:
        genre = request.form["genre"]
    except KeyError:
        genre = None

    try:
        if not title and not genre:
            flash("Title or genre is required.", 'error')
            return redirect("/search")

        all_movies = get_all_movies()

        if not all_movies["success"]:
            print(all_movies["error"])
            return render_template("error.html", error=all_movies["error"])

        filtered_by_title = []

        if title and isinstance(title, str):
            for movie in all_movies["data"]:
                if title.lower() in movie["title"].lower():
                    filtered_by_title.append(movie)

        else:
            filtered_by_title = all_movies["data"]

        filtered_by_genre = []

        if genre and isinstance(genre, str):
            for movie in filtered_by_title:
                if genre.lower() in movie["genre_id"].lower():
                    filtered_by_genre.append(movie)

        else:
            filtered_by_genre = filtered_by_title

        movie_ids = []

        for movie in filtered_by_genre:
            movie_ids.append(movie["id"])

        return redirect("/search/results/{}".format(",".join(movie_ids)))

    except Exception as e:
        print(e)
        flash("Search failed. {}".format(e), 'error')
        return redirect("/search")
