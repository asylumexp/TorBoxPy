from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    """Represents a TorBox response."""

    success: Optional[bool] = None
    error: Optional[str] = None
    detail: Optional[str] = None


class ResponseData(Response[T]):
    """Represents a TorBox response containing data."""

    data: Optional[T] = None  # Data of type T if available
