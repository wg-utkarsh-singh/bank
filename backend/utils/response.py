from functools import wraps

from flask import jsonify
from werkzeug import Response
from werkzeug.datastructures import Headers


def resolve_schema_instance(schema):
    return schema() if isinstance(schema, type) else schema


def unpack_tuple_response(rv):
    status = headers = None

    # unpack tuple returns
    # Unlike Flask, we check exact type because tuple subclasses may be
    # returned by view functions and paginated/dumped
    if type(rv) is tuple:
        len_rv = len(rv)

        # a 3-tuple is unpacked directly
        if len_rv == 3:
            rv, status, headers = rv
        # decide if a 2-tuple has status or headers
        elif len_rv == 2:
            if isinstance(rv[1], (Headers, dict, tuple, list)):
                rv, headers = rv
            else:
                rv, status = rv
        # other sized tuples are not allowed
        else:
            raise TypeError(
                "The view function did not return a valid response tuple."
                " The tuple must have the form (body, status, headers),"
                " (body, status), or (body, headers)."
            )

    return rv, status, headers


def set_status_and_headers_in_response(response, status, headers):
    if headers:
        response.headers.extend(headers)
    if status is not None:
        if isinstance(status, int):
            response.status_code = status
        else:
            response.status = status


def response(status_code, schema=None):
    schema = resolve_schema_instance(schema)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result_raw, r_status_code, r_headers = unpack_tuple_response(
                func(*args, **kwargs)
            )
            # If return value is a werkzeug Response, return it
            if isinstance(result_raw, Response):
                set_status_and_headers_in_response(result_raw, r_status_code, r_headers)
                return result_raw

            # Dump result with schema if specified and status code matches
            if schema is None or r_status_code != status_code:
                result_dump = result_raw
            else:
                result_dump = schema.dump(result_raw)

            # Build response
            resp = jsonify(result_dump)
            set_status_and_headers_in_response(resp, r_status_code, r_headers)
            if r_status_code is None:
                resp.status_code = status_code

            return resp

        return wrapper

    return decorator
