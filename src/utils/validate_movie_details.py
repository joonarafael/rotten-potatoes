"""Module to house the sanity-check-function to validate user input
for adding/editing movies."""

# pylint: disable=import-error
# pylint: disable=broad-exception-caught


from datetime import datetime
from flask import flash
from sql.genres import get_all_genres


def validate_movie_details(
        title: str,
        genre: str,
        description: str,
        year: str) -> bool:
    """Function to validate user input for adding/editing movies.

    Args:
        title (str): Movie title as a string (4-64 chars)
        genre (str): Movie genre ID as a string (checked against the genres table)
        description (str): Movie description as a string (4-1024 chars)
        year (str): Movie release year as a string (converted to an int later,
        acceptable: 1900 to current year)

    Returns:
        bool: Whether or not the input is valid.
    """
    genres = get_all_genres()

    if not genres["success"]:
        print(genres["error"])

        flash(
            "An error occurred while fetching genres. Please try again later.",
            'error')

        return False

    genre_ids = [genre["id"] for genre in genres["data"]]

    if not title or not genre or not description or not year:
        flash("Title, genre, description and year are required.", 'error')
        return False

    if not isinstance(
            title,
            str) or not isinstance(
            genre,
            str) or not isinstance(
                description,
                str) or not isinstance(
                    year,
            str):
        flash("Title, genre, description and year must be of type string.", 'error')
        return False

    if len(title) < 4 or len(title) > 64:
        flash("Title must be between 4 and 64 characters.", 'error')
        return False

    if len(description) < 4 or len(description) > 1024:
        flash("Description must be between 4 and 1024 characters.", 'error')
        return False

    if genre not in genre_ids:
        flash("Unknown genre.", 'error')
        return False

    year_as_int = int(year)

    if year_as_int < 1900 or year_as_int > datetime.now().year:
        flash(
            f"Year must be between greater than 1900 and equal to or less than {datetime.now().year}.",
            'error')
        return False

    return True
