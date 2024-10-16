"""SQL module for genre-related stuff."""

# pylint: disable=import-error
# pylint: disable=broad-exception-caught


from sqlalchemy import text
from db import db
from structs import SQLOperationResult


def get_all_genres() -> SQLOperationResult:
    """Function to retrieve all genres from the database.

    Returns:
        SQLOperationResult: SQL Operation Result.
    """
    try:
        sql = text(
            "SELECT * FROM genres ORDER BY name ASC")
        result = db.session.execute(sql)
        genres = result.fetchall()

        if genres is not None:
            genres_as_dicts = []

            for genre in genres:
                genre_dict = {
                    "id": str(genre[0]),
                    "name": genre[1]
                }

                genres_as_dicts.append(genre_dict)

            return {
                "success": True,
                "error": None,
                "data": genres_as_dicts
            }

        return {
            "success": False,
            "error": "No genres found.",
            "data": None
        }

    except Exception as e:
        print("DB Function 'get_all_genres()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }
