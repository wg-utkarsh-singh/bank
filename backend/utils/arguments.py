from functools import wraps

from webargs.flaskparser import FlaskParser

ARGUMENTS_PARSER = FlaskParser()


def arguments(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            return func(*f_args, **f_kwargs)

        # Call use_args (from webargs) to inject params in function
        return ARGUMENTS_PARSER.use_args(schema)(wrapper)

    return decorator
