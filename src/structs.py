"""Module for custom types & structs."""


from typing import TypedDict


class SQLOperationResult(TypedDict):
    """Simple typed dictionary for SQL operation results."""
    success: bool
    error: str | None
    data: dict | list[dict] | None
