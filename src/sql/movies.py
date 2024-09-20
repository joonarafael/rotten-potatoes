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
                genre_dict = {
                    "id": str(movie[0]),
                    "title": movie[1],
                    "description": movie[2],
                    "year": movie[3],
                    "genre_id": str(movie[4]),
                    "created_by": str(movie[5]),
                    "created_at": movie[6].isoformat(),
                    "updated_at": movie[7].isoformat()
                }

                movies_as_dicts.append(genre_dict)

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
        print("DB Function 'register()' failed.")
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
    