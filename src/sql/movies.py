from structs import SQLOperationResult
from db import db
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from flask import session


def get_all_movies() -> SQLOperationResult:
    try:
        sql = text(
            "SELECT * FROM movies ORDER BY title ASC")
        result = db.session.execute(sql)
        movies = result.fetchall()

        if movies is not None:
            movies_as_dicts = []

            for movie in movies:
                movie_dict = {
                    "id": str(movie[0]),
                    "title": movie[1],
                    "description": movie[2],
                    "year": movie[3],
                    "genre_id": str(movie[4]),
                    "created_by": str(movie[5]),
                    "created_at": movie[6].isoformat(),
                    "updated_at": movie[7].isoformat()
                }

                ratings = get_movie_ratings_by_id(movie_dict["id"])

                if ratings["success"]:
                    movie_dict["reviews"] = ratings["data"]
                    movie_dict["review_count"] = len(ratings["data"])

                    if movie_dict["review_count"] > 0:
                        movie_dict["review_average"] = sum([review["rating"] for review in ratings["data"]]) / len(ratings["data"])
                    else:
                        movie_dict["review_average"] = None
                else:
                    movie_dict["reviews"] = []
                    movie_dict["review_count"] = 0
                    movie_dict["review_average"] = None

                movies_as_dicts.append(movie_dict)

            return {
                "success": True,
                "error": None,
                "data": movies_as_dicts
            }

        return {
            "success": False,
            "error": "No movies found.",
            "data": None
        }

    except Exception as e:
        print("DB Function 'get_all_movies()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }
    

def get_movie_by_id(id: str) -> SQLOperationResult:
    try:
        sql = text(
            "SELECT * FROM movies WHERE id = :id")
        result = db.session.execute(sql, {"id": id})
        movie = result.fetchone()

        if movie is not None:
            movie_dict = {
                "id": str(movie[0]),
                "title": movie[1],
                "description": movie[2],
                "year": movie[3],
                "genre_id": str(movie[4]),
                "created_by": str(movie[5]),
                "created_at": movie[6].isoformat(),
                "updated_at": movie[7].isoformat()
            }

            ratings = get_movie_ratings_by_id(movie_dict["id"])

            if ratings["success"]:
                movie_dict["reviews"] = ratings["data"]
                movie_dict["review_count"] = len(ratings["data"])
                
                if movie_dict["review_count"] > 0:
                    movie_dict["review_average"] = sum([review["rating"] for review in ratings["data"]]) / len(ratings["data"])
                else:
                    movie_dict["review_average"] = None
            else:
                movie_dict["reviews"] = []
                movie_dict["review_count"] = 0
                movie_dict["review_average"] = None

            return {
                "success": True,
                "error": None,
                "data": movie_dict
            }

        return {
            "success": False,
            "error": "No movies found.",
            "data": None
        }

    except Exception as e:
        print("DB Function 'get_movie_by_id()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }


def delete_movie_by_id(id: str, as_admin: bool) -> SQLOperationResult:
    try:
        movie = get_movie_by_id(id)

        if movie["success"]:
            ratings = get_movie_ratings_by_id(movie["data"]["id"])

            # check if people have rated the movie
            if ratings["success"]:
                ratings_count = len(ratings["data"])

                # movie has reviews, enter deletion logic
                if ratings_count > 1:
                    if as_admin:
                        sql = text(
                            "DELETE FROM movies WHERE id = :id")
                        db.session.execute(sql, {"id": id})
                        db.session.commit()

                    else:
                        return {
                            "success": False,
                            "error": "Movie has reviews from other people. Only an admin can delete this.",
                            "data": None
                        }

                # if the only review is by the user itself, delete the movie
                elif ratings_count == 1:
                    if ratings["data"][0]["user_id"] == session["user_id"] or as_admin:
                        sql = text(
                            "DELETE FROM movies WHERE id = :id")
                        db.session.execute(sql, {"id": id})
                        db.session.commit()
                    else:
                        return {
                            "success": False,
                            "error": "Movie has reviews from other people. Only an admin can delete this.",
                            "data": None
                        }

                # no reviews, delete the movie straight away
                sql = text(
                    "DELETE FROM movies WHERE id = :id")
                db.session.execute(sql, {"id": id})
                db.session.commit()

                return {
                    "success": True,
                    "error": None,
                    "data": None
                }
            
            sql = text(
                "DELETE FROM movies WHERE id = :id")
            db.session.execute(sql, {"id": id})
            db.session.commit()

            return {
                "success": True,
                "error": None,
                "data": None
            }

        return {
            "success": False,
            "error": "Movie fetching with given ID was unsuccessful.",
            "data": None
        }

    except Exception as e:
        print("DB Function 'delete_movie_by_id()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }


def add_movie(title: str, genre: str, description: str, year: int, user_id: str) -> SQLOperationResult:
    try:
        # incoming data has been already validated in the route
        # it's safe to insert it into the database
        sql = text(
            "INSERT INTO movies (title, genre_id, description, year, created_by) VALUES (:title, :genre_id, :description, :year, :created_by)")
        db.session.execute(
            sql, {"title": title, "genre_id": genre, "description": description, "year": year, "created_by": user_id})
        db.session.commit()

        return {
            "success": True,
            "error": None,
            "data": None
        }

    except Exception as e:
        print("DB Function 'add_movie()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }
    

def rate_movie(id: str, rating: int, comment: str, user_id: str) -> SQLOperationResult:
    try:
        # check if user has already reviewed the movie
        sql = text(
            "SELECT * FROM reviews WHERE movie_id = :movie_id AND user_id = :user_id")
        result = db.session.execute(sql, {"movie_id": id, "user_id": user_id})
        rating_exists = result.fetchone()

        if rating_exists is not None:
            return {
                "success": False,
                "error": "User has already rated the movie.",
                "data": None
            }
        
        # incoming data has been already validated in the route
        # it's safe to insert it into the database
        sql = text(
            "INSERT INTO reviews (movie_id, user_id, rating, comment) VALUES (:movie_id, :user_id, :rating, :comment)")
        db.session.execute(
            sql, {"movie_id": id, "user_id": user_id, "rating": rating, "comment": comment})
        db.session.commit()

        return {
            "success": True,
            "error": None,
            "data": None
        }

    except Exception as e:
        print("DB Function 'rate_movie()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }
    

def edit_movie_by_id(id: str, title: str, genre: str, description: str, year: int) -> SQLOperationResult:
    try:
        # incoming data has been already validated in the route!
        # it's safe to insert it into the database
        sql = text(
            "UPDATE movies SET title = :title, genre_id = :genre_id, description = :description, year = :year WHERE id = :id")
        db.session.execute(
            sql, {"title": title, "genre_id": genre, "description": description, "year": year, "id": id})
        db.session.commit()

        return {
            "success": True,
            "error": None,
            "data": None
        }

    except Exception as e:
        print("DB Function 'edit_movie_by_id()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }


def get_movie_ratings_by_id(id: str) -> SQLOperationResult:
    try:
        # check if user has already reviewed the movie
        sql = text(
            "SELECT * FROM reviews WHERE movie_id = :movie_id")
        result = db.session.execute(sql, {"movie_id": id})
        ratings = result.fetchall()

        if ratings is not None:
            ratings_as_dicts = []

            for rating in ratings:
                rating_dict = {
                    "id": str(rating[0]),
                    "user_id": str(rating[1]),
                    "movie_id": str(rating[2]),
                    "rating": rating[3],
                    "comment": rating[4],
                    "created_at": rating[5].isoformat(),
                    "updated_at": rating[6].isoformat()
                }

                ratings_as_dicts.append(rating_dict)

            return {
                "success": True,
                "error": None,
                "data": ratings_as_dicts
            }

        return {
            "success": True,
            "error": "No ratings found.",
            "data": []
        }

    except Exception as e:
        print("DB Function 'get_movie_ratings_by_id()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }


def get_rating_by_id(id: str) -> SQLOperationResult:
    try:
        sql = text(
            "SELECT * FROM reviews WHERE id = :id")
        result = db.session.execute(sql, {"id": id})
        rating = result.fetchone()

        if rating is not None:
            rating_dict = {
                "id": str(rating[0]),
                "user_id": str(rating[1]),
                "movie_id": str(rating[2]),
                "rating": rating[3],
                "comment": rating[4],
                "created_at": rating[5].isoformat(),
                "updated_at": rating[6].isoformat()
            }

            return {
                "success": True,
                "error": None,
                "data": rating_dict
            }

        return {
            "success": True,
            "error": "No rating found.",
            "data": []
        }

    except Exception as e:
        print("DB Function 'get_rating_by_id()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }
    
def delete_rating_by_id(id: str, as_admin: bool) -> SQLOperationResult:
    try:
        rating = get_rating_by_id(id)

        if rating["success"]:
            if rating["data"]["user_id"] == session["user_id"] or as_admin:
                sql = text(
                    "DELETE FROM reviews WHERE id = :id")
                db.session.execute(sql, {"id": id})
                db.session.commit()

                return {
                    "success": True,
                    "error": None,
                    "data": None
                }

            return {
                "success": False,
                "error": "You are not allowed to delete this review!",
                "data": None
            }

        return {
            "success": False,
            "error": "Rating fetching with given ID was unsuccessful.",
            "data": None
        }

    except Exception as e:
        print("DB Function 'delete_rating_by_id()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }