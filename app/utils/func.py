from functools import wraps
from flask import current_app, jsonify


def handle_db_errors(default_response=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                current_app.logger.error(f"Database error in {func.__name__}: {str(e)}")
                # Return a default or raise again
                if default_response is not None:
                    return default_response
                return None

        return wrapper

    return decorator
