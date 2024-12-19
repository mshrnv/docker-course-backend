from typing import Final

from fastapi import HTTPException, status


class DatabaseError(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Произошла ошибка в базе данных: {message}"

    def __init__(self, message: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(message=message)
        super().__init__(self.message)


class CredentialsException(HTTPException):
    def __init__(self, detail: str) -> None:
        self.detail = detail

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class Error(BaseException):
    """Базовое исключение для всех ошибок"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)



class ForeignKeyViolationError(BaseException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFound(BaseException):
    """Исключение, вызываемое, если программа не найдена."""
    def __init__(self, message: str = "Not found"):
        self.message = message
        super().__init__(message)


class AlreadyExists(BaseException):
    """Исключение, вызываемое, если программа уже существует."""
    def __init__(self, message: str = "Already exists"):
        self.message = message
        super().__init__(message)