
import app.common.constants as C
from flask import Response
from flask_httpauth import HTTPTokenAuth

sample_apikey_auth = HTTPTokenAuth(header=C.X_API_KEY)


@sample_apikey_auth.verify_token
def verify_token(token):
    apikey = C.CORRECT_APIKEY
    if token == apikey:
        return True
    return False


@sample_apikey_auth.error_handler
def apikey_auth_error(status):
    return Response(status=status, response="Authorization Problem")

