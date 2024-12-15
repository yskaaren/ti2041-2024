from ninja.security import HttpBearer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            # Decodificar y verificar el token JWT
            decoded_token = AccessToken(token)
            return decoded_token
        except Exception as e:
            raise AuthenticationFailed("Token no válido o expirado.")
