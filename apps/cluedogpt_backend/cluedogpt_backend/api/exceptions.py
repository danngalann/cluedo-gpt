"""
Custom exceptions for the application.
"""


class BadRequestError(Exception):
    """
    Custom exception for validation errors.
    This will be caught by the error handling middleware and converted to a 400 Bad Request.
    """

    def __init__(self, message: str, details: str | None = None, error_code: str | None = None):
        """
        Initialize validation exception.

        Args:
            message: The validation error message
            details: Optional additional details
        """
        self.message = message
        self.details = details
        self.error_code = error_code
        super().__init__(message)


class BusinessLogicError(Exception):
    """
    Custom exception for business logic errors.
    This will be caught by the error handling middleware and converted to a 400 Bad Request.
    """

    def __init__(self, message: str, details: str | None = None):
        """
        Initialize business logic exception.

        Args:
            message: The business logic error message
            details: Optional additional details
        """
        self.message = message
        self.details = details
        super().__init__(message)


class ResourceNotFoundError(Exception):
    """
    Custom exception for resource not found errors.
    This will be caught by the error handling middleware and converted to a 404 Not Found.
    """

    def __init__(self, error_code: str, message: str, details: str | None = None):
        """
        Initialize resource not found exception.

        Args:
            message: The error message
            details: Optional additional details
        """
        self.message = message
        self.details = details
        self.error_code = error_code
        super().__init__(message)


class ServerError(Exception):
    """
    Custom exception for server errors.
    This will be caught by the error handling middleware and converted to a 500 Internal Server Error.
    """

    def __init__(self, message: str, details: str | None = None, error_code: str | None = None):
        """
        Initialize server error exception.

        Args:
            message: The server error message
            details: Optional additional details
            error_code: Optional error code
        """
        self.message = message
        self.details = details
        self.error_code = error_code
        super().__init__(message)
