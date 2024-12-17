from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User


class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token.get("user_id")
            if not user_id:
                raise AuthenticationFailed("Token no contiene ID de usuario.")
            user = User.objects.get(id=user_id)

            return user
        except Exception as e:
            raise AuthenticationFailed("Token no válido o expirado.")
