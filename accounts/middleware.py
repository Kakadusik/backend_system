from django.utils.functional import SimpleLazyObject
import jwt
from accounts.models import User
from backend_system import settings


class AnonymousUser():
    """
    Анонимный пользователь для JWT
    """
    def is_authenticated(self):
        return False
                
def get_user_from_jwt(request):
    auth_header = request.headers.get('Authorization') # получаем заголовок Authorization из запроса
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1] # получаем токен из заголовка
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            if user_id:
                try:
                    return User.objects.get(id=user_id, is_active=True)
                except User.DoesNotExist:
                    pass
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            pass
    return AnonymousUser()

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: get_user_from_jwt(request))
        return self.get_response(request)