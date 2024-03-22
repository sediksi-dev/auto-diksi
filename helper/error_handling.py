class BaseCustomException(Exception):
    """Base class for custom exception classes."""

    def __init__(self, message: str, func: str = None):
        self.message = message
        self.func = func
        self.__status_code = self.status_code if hasattr(self, "status_code") else 500
        super().__init__(self.message)

    @property
    def status_code(self):
        return self.__status_code

    def __str__(self):
        func = f" on `{self.func}`" if self.func else ""
        msg = f"[{self.prefix}] {self.message}{func} ({self.__status_code})"
        return msg


class AiResponseException(BaseCustomException):
    """Exception for errors related to AI responses."""

    status_code = 511
    prefix = "AI_ERROR"


class WpException(BaseCustomException):
    """Exception for errors related to WordPress interactions."""

    status_code = 512
    prefix = "WORDPRESS_ERROR"


class DatabaseException(BaseCustomException):
    """Exception for errors related to database operations."""

    status_code = 513
    prefix = "DATABASE_ERROR"


def error_handler(type, msg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if type == "ai":
                    raise AiResponseException(f"{msg} >>> {str(e)}")
                elif type == "wp":
                    raise WpException(f"{msg} >>> {str(e)}")
                elif type == "db":
                    raise DatabaseException(f"{msg} >>> {str(e)}")
                else:
                    raise e

        return wrapper

    return decorator
