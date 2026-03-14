from django.shortcuts import render
from psycopg2 import IntegrityError
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.jwt import create_jwt_token
from accounts.models import User
from accounts.serializers import LoginSerializer, RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        if request.data.user.is_authenticated:
            return Response({'error': 'Пользователь уже зарегистрирован'}, status=status.HTTP_403_FORBIDDEN)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except IntegrityError:
                return Response({'error': 'Пользователь с таким email уже существует'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "patronymic": user.patronymic,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = create_jwt_token(user)
            return Response({'token': token, 'user_id': user.id})
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # разрешаем только авторизованным пользователям

    def post(self, request):
        return Response({'message': 'Выход осуществлен успешно'}) # клиент должен удалить токен
    
# LoginView без сериализатора (предыдущий вариант)   
# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         if not email or not password:
#             return Response({'error': 'Email и пароль - обязательные поля'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             user = User.objects.get(email=email, is_active=True)
#         except User.DoesNotExist:
#             return Response({'error': 'Пользователь не найден'}, status=status.HTTP_401_UNAUTHORIZED) # можно заменить на сообщение 'Неверный логин или пароль'
        
#         if not user.check_password(password):
#             return Response({'error': 'Неверный пароль'}, status=status.HTTP_401_UNAUTHORIZED) # можно заменить на сообщение 'Неверный логин или пароль'
        
#         token = create_jwt_token(user)
#         return Response({'token': token, 'user_id': user.id})    