"""Authentication classes for channels."""
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError
from jwt import decode as jwt_decode
from rest_framework_simplejwt.tokens import UntypedToken

User = get_user_model()

def Convert(tup):
    di = {}
    for a, b in tup:
        di.setdefault(a, []).append(b)
    return di


class JWTAuthMiddleware:
    """Middleware to authenticate user for channels"""

    def __init__(self, app):
        """Initializing the app."""
        self.app = app

    async def __call__(self, scope, receive, send):
        """Authenticate the user based on jwt."""
        close_old_connections()
        try:
            # Decode the query string and get token parameter from it.
            # token = parse_qs(scope["query_string"].decode("utf8")).get('token', None)[0]

            # Decode the headers and get the token parameter from the Authorization header.
            # token_list = Convert(scope.get('headers', [])).get(b'authorization', b'')
            # token = token_list[0].decode("utf-8")

           # Get token from header
            headers = dict(scope["headers"])
            token = headers[b"authorization"].decode()

            # Decode the token to get the user id from it.
            data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Get the user from database based on user id and add it to the scope.
            scope['user'] = await self.get_user(data['user_id'])
        except (TypeError, KeyError, InvalidSignatureError, ExpiredSignatureError, DecodeError):
            # Set the user to Anonymous if token is not valid or expired.
            scope['user'] = AnonymousUser()
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        """Return the user based on user id."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    """This function wrap channels authentication stack with JWTAuthMiddleware."""
    return JWTAuthMiddleware(AuthMiddlewareStack(app))