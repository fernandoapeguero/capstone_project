import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os
# os.environ['AUTH_DOMAIN']
AUTH0_DOMAIN = 'auth0-fsnd.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'nba_data_api'
# os.environ['API_AUDIENCE']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():

    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'Authorization Header Missing',
            'description': 'Authorization header is expected'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'Invalid Header',
            'description': 'Token must be a Bearer Token'
        }, 401)

    if len(parts) == 1:
        raise AuthError({
            'code': 'Invalid Token',
            'description': 'Invalid Token'
        }, 401)

    if len(parts) > 2:
        raise AuthError({
            'code': 'invalid token',
            'description': 'Token must be a Bearer Token'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):

    if 'permissions' not in payload:
        raise AuthError({
            'code': 'Invalid Claims',
            'description': 'Permissions not included in JWT'
        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                             "description":
                             "incorrect claims,"
                             "please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                             "description":
                             "Unable to parse authentication"
                             " token."}, 401)
    raise AuthError({"code": "invalid_header",
                     "description": "Unable to find appropriate key"}, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
