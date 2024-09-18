from structs import SQLOperationResult
from db import db
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from flask import session


def register(username: str, password: str) -> SQLOperationResult:
    try:
        hashed_password = generate_password_hash(password)

        sql = text(
            "INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(
            sql, {"username": username, "password": hashed_password})

        db.session.commit()

        return {
            "success": True,
            "error": None,
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

def logout() -> None:
    del session["csrf_token"]
    del session["is_admin"]
    del session["user_id"]
    del session["username"]