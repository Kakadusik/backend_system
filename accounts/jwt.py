from django.conf import settings
import jwt
from datetime import datetime, timezone

def create_jwt_token(user):
    """
    Генерирует JWT-токен для пользователя.
    """
    now_utc = datetime.now(timezone.utc)
    payload = {
        'user_id': user.id,
        'exp': now_utc + settings.JWT_EXPIRATION_DELTA,
        'iat': now_utc,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token