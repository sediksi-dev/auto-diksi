class AiResponseException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[AI_RESPONSE_ERROR] Error When Processing AI Response: {self.message}"


class WpException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[WP_RESPONSE_ERROR] Error When Communicating with WordPress: {self.message}"


class DatabaseException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return (
            f"[DATABASE_ERROR] Error When Communicating with Database: {self.message}"
        )


def error_handler(type, msg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if type == "ai":
                    raise AiResponseException(502, f"{msg}. Reason: {str(e)}")
                elif type == "wp":
                    raise WpException(502, f"{msg}. Reason: {str(e)}")
                elif type == "db":
                    raise DatabaseException(502, f"{msg}. Reason: {str(e)}")
                else:
                    raise e

        return wrapper

    return decorator
