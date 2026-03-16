import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from .models import User

class JWTAuthentication(BaseAuthentication):
    """
    Класс авторизации на основе JWT
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # анонимный пользователь

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            if not user_id:
                return None
            try:
                user = User.objects.get(id=user_id, is_active=True)
            except User.DoesNotExist:
                return None
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

        return (user, None)