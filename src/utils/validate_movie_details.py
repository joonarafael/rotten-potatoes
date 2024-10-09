from sql.genres import get_all_genres
from flask import flash
from datetime import datetime

def validate_movie_details(title: str, genre: str, description: str, year: str) -> bool:
    genres = get_all_genres()

    if not genres["success"]:
        print(genres["error"])

        flash("An error occurred while fetching genres. Please try again later.", 'error')

        return False
    
    genre_ids = [genre["id"] for genre in genres["data"]]

    if not title or not genre or not description or not year:
        flash("Title, genre, description and year are required.", 'error')
        return False
    
    if not isinstance(title, str) or not isinstance(genre, str) or not isinstance(description, str) or not isinstance(year, str):
        flash("Title, genre, description and year must be of type string.", 'error')
        return False
    
    if len(title) < 4 or len(title) > 64:
        flash("Title must be between 4 and 64 characters.", 'error')
        return False
    
    if genre not in genre_ids:
        flash("Unknown genre.", 'error')
        return False
    
    year_as_int = int(year)
    
    if year_as_int < 1900 or year_as_int > datetime.now().year:
        flash("Year must be between greater than 1900 and equal to or less than {}.".format(datetime.now().year), 'error')
        return False
    
    return True