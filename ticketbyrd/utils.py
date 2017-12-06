from flask import request, jsonify
import datetime
import functools
import jwt
import logging
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
)

log = logging.getLogger(__name__)

def generate_jwt(**kwargs):
    """Generate a jwt token."""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }
    payload.update(**kwargs)
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token.decode()

def _validate_token(headers):
    """Validate the token inside the headers.
    Return the payload if correct, None in the other cases.
    The payload contains the token.
    """
    payload = None
    if "Authorization" in headers:
        try:
            encoded = headers['Authorization'].split('Bearer ')[1]
            payload = jwt.decode(encoded, 'secret', algorithm='HS256')
        except (IndexError, DecodeError, ExpiredSignatureError):
            log.info("Attempt to login with non valid/expired token.")
    return payload




def token_required(func):
    """Check if the given jwt is valid."""
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        # check if user is logged
        payload = _validate_token(request.headers)

        if payload is None:
            return jsonify({"message": "User not authorized."}), 401
        else:
            return func(*args, **kwargs)
    return wrapped

