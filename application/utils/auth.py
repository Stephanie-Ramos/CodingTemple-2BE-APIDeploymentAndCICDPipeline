# This imports three date/time tools from Python’s built-in datetime module
# datetime: represents a specific date and time and is used when setting the token’s creation or expiration time
# timedelta: represents an amount of time, such as one hour, so your token can expire after a set period
# timezone: lets you work with timezone-aware timestamps, typically UTC
from datetime import datetime, timedelta, timezone
# current_app: Retrieve the secret key loaded from config.py file. That secret key is then used to sign and verify your JWT
# jsonify: converts Python data into a JSON response
# request: represents the incoming HTTP request. Authentication decorator uses it to retrieve the Bearer Token from the request headers
from flask import current_app, jsonify, request
# These come from the python-jose package
# jwt: provides the methods used to encode and decode JSON Web Tokens
# JWTError: represents errors that can occur while validating a token. For example, a token may be expired, modified, incorrectly formatted, or signed with the wrong secret key
from jose import jwt, JWTError
# wraps: comes from Python's built-in functools module. It is used when creating the custom decorator
# @wraps(f): is to preserve information about the original route function being decorated
from functools import wraps


def encode_token(customer_id):
    payload = {
        # stores the logged-in customer's ID inside the token 
        "customer_id": customer_id,
        # makes the token expire after one hour 
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    # creates the actual JWT token
    # The encode() method takes information about the customer and converts it into a signed JSON Web Token (JWT)
    token = jwt.encode(
        # payload contains the information is stored inside the JWT
        # This allows your application to later determine which customer the token belongs to
        payload,
        # This retrieves your secret key from Flask's configuration
        current_app.config["SECRET_KEY"],
        # This tells python-jose which cryptographic algorithm to use to sign the JWT
        algorithm="HS256"
    )

    return token



def token_required(f):
    # Without @wraps(f), Flask may see the wrapper function's name instead of get_my_tickets, 
    # which can cause problems when multiple routes use the same decorator
    @wraps(f)
    def decorated(*args, **kwargs):
        # looks for a request header like: Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "message": "Authorization token is missing"
            }), 401

        try:
            # takes this: Bearer eyJhbGciOiJIUzI1NiIs...
            # and splits it into: ["Bearer", "eyJhbGciOiJIUzI1NiIs..."]
            # Index [1] gives us just the token.
            token = auth_header.split(" ")[1]

            # checks that the JWT was created with your application's secret key and that it hasn't expired
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            # inside the JWT, this line retrieves it: 
            customer_id = payload["customer_id"]

        # handles several possible problems 
        # JWTError    → invalid or expired JWT
        # IndexError  → malformed Authorization header
        # KeyError    → token does not contain customer_id
        except (JWTError, IndexError, KeyError):
            return jsonify({
                "message": "Invalid or expired token"
            }), 401

        # calls the protected route and passes the logged-in customer's ID into it 
        return f(customer_id, *args, **kwargs)

    return decorated