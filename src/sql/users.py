from structs import SQLOperationResult
from db import db
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash
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
    
def login(username, password) -> SQLOperationResult:
    sql = text("SELECT id, created_at, updated_at, password, is_admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user is not None:
        user_dict = {
            "id": str(user[0]),
            "created_at": user[1].isoformat(),
            "password": user[3],
            "updated_at": user[2].isoformat(),
            "username": username,
            "is_admin": user[4]
        }

        if check_password_hash(user_dict["password"], password):
            session["csrf_token"] = urandom(16).hex()
            session["is_admin"] = user[2]
            session["user_id"] = user[1]
            session["username"] = username

            return {
                "success": True,
                "error": None,
                "data": user_dict
            }

    return {
        "success": False,
        "error": "No user named '{}'.".format(username),
        "data": None
    }

def logout() -> None:
    def remove_key_from_session(key: str):
        try:
            del session[key]
        except KeyError:
            pass

    remove_key_from_session("csrf_token")
    remove_key_from_session("is_admin")
    remove_key_from_session("user_id")
    remove_key_from_session("username")
