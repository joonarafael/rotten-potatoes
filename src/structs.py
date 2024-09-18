from typing import TypedDict


class SQLOperationResult(TypedDict):
    success: bool
    error: str | None
    data: dict | None
