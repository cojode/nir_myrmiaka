from enum import Enum


class BaseErrorType(str, Enum):
    REPOSITORY_ERROR = "repository_error"
    DOMAIN_ERROR = "domain_error"
    SCHEMA_ERROR = "schema_error"


class BaseError(Exception):
    """
    Base class for all custom exceptions in the application that
    have a message and optional data.
    This class inherits from the built-in Exception class.
    """

    def __init__(
        self, error: BaseErrorType, message: str, detail: dict | None = None
    ):
        super().__init__(message)
        self.message = message
        self.error = error
        self.detail = detail or {}


class RepositoryError(BaseError):
    """
    Base class for all repository-related exceptions.
    This class inherits from the built-in Exception class.
    """

    def __init__(
        self,
        message: str,
        detail: dict | None = None,
    ):
        super().__init__(BaseErrorType.REPOSITORY_ERROR, message, detail)


class DomainError(BaseError):
    """
    Base class for all domain-related exceptions.
    This class inherits from the built-in Exception class.
    """

    def __init__(
        self,
        message: str,
        detail: dict | None = None,
    ):
        super().__init__(BaseErrorType.DOMAIN_ERROR, message, detail)


class SchemaError(BaseError):
    """
    Base class for all schema-related exceptions.
    This class inherits from the built-in Exception class and
    ValidationError from Pydantic.
    """

    def __init__(
        self,
        message: str,
        detail: dict | None = None,
    ):
        super().__init__(BaseErrorType.SCHEMA_ERROR, message, detail)
