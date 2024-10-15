"""SQL module for user-related and auth-related stuff."""

# pylint: disable=import-error
# pylint: disable=broad-exception-caught

# pylint: disable=redefined-builtin
# i want to use `id` as variable name but pylint ain't having it


from os import urandom
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from db import db
from structs import SQLOperationResult


def get_user_by_id(id: str) -> SQLOperationResult:
    """Function to retrieve a user by their ID.

    Args:
        id (str): User ID as a string.

    Returns:
        SQLOperationResult: SQL Operation Result.
    """
    try:
        sql = text(
            "SELECT id, created_at, updated_at, username, is_admin FROM users WHERE id=:id")
        result = db.session.execute(sql, {"id": id})
        user = result.fetchone()

        if user is not None:
            user_dict = {
                "id": id,
                "created_at": user[1].isoformat(),
                "updated_at": user[2].isoformat(),
                "username": user[3],
                "is_admin": user[4]
            }

            return {
                "success": True,
                "error": None,
                "data": user_dict
            }

        return {
            "success": False,
            "error": f"No user with id '{id}'.",
            "data": None
        }

    except Exception as e:
        print("DB Function 'get_user_by_id()' failed.")
        print(e)

        return {
            "success": False,
            "error": str(e),
            "data": None
        }


def register(username: str, password: str) -> SQLOperationResult:
    """Function to register a new user.

    Args:
        username (str): Username as a string.
        password (str): Password (still in plaintext) as a string.

    Returns:
        SQLOperationResult: SQL Operation Result.
    """
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


def login(username: str, password: str) -> SQLOperationResult:
    """Function for logging in a user.

    Args:
        username (str): Username as a string.
        password (str): Password (in plaintext) as a string.

    Returns:
        SQLOperationResult: SQL Operation Result.
    """
    sql = text(
        "SELECT id, created_at, updated_at, password, is_admin FROM users WHERE username=:username")
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
            # initialize session
            session["csrf_token"] = urandom(16).hex()
            session["is_admin"] = user_dict["is_admin"]
            session["user_id"] = user_dict["id"]
            session["username"] = user_dict["username"]

            del user_dict["password"]

            return {
                "success": True,
                "error": None,
                "data": user_dict
            }

    return {
        "success": False,
        "error": "Username or password incorrect.",
        "data": None
    }


def logout() -> None:
    """Function to log out a user & clear the session.
    """
    def remove_key_from_session(key: str):
        try:
            del session[key]
        except KeyError:
            pass

    remove_key_from_session("csrf_token")
    remove_key_from_session("is_admin")
    remove_key_from_session("user_id")
    remove_key_from_session("username")
