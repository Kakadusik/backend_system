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
        fields = ['email', 'first_name', 'last_name', 'patronymic', 'password', 'password2']

    def _validate_name_part(self, value, field_name):
        """
        Валидация имени или фамилии
        """

        if not value.strip():
            raise serializers.ValidationError(f'{field_name} не может быть пустым или состоять из пробелов')
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError(f'{field_name} не может содержать цифры')
        return value

    def validate_email(self, value):
        return value.lower() # переводим email в нижний регистр

    def validate_first_name(self, value):
        return self._validate_name_part(value, 'Имя')
    
    def validate_last_name(self, value):
        return self._validate_name_part(value, 'Фамилия')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password':'Пароли не совпадают'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя
    """

    email = serializers.EmailField(error_messages={'required': 'Email обязателен'})
    password = serializers.CharField(write_only=True, error_messages={'required': 'Пароль обязателен'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверные учётные данные")
        if not user.check_password(password):
            raise serializers.ValidationError("Неверные учётные данные")
        data['user'] = user
        return data