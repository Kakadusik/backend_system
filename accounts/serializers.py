from rest_framework import serializers

from accounts.models import User


class RegisterSerializer(serializers.ModelSeralizer):
    """
    Сериализатор для регистрации пользователя
    """

    password = serializers.CharField(write_only=True, min_length=8, max_length=128, style={'input': 'password'}) # пароль не передается в ответе
    password2 = serializers.CharField(write_only=True, min_length=8, max_length=128, style={'input': 'password'}) # пароль для подтверждения

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'password', 'password2')

        def validate(self, data):
            if data['password'] != data['password2']:
                raise serializers.ValidationError('Пароли не совпадают')
            

