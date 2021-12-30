from functools import wraps

from structlog import get_logger

logger = get_logger()


def log():
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            logger.info(f"{function.__name__}.starts")

            result = function(*args, **kwargs)

            logger.info(f"{function.__name__}.stops")

            return result

        return inner

    return wrapper
