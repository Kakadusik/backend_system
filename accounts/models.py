from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import bcrypt


class UserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User, отвечает за создание пользователей
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Функция создания пользователя
        """

        if not email: # проверка, что email передан
            raise ValueError('Пользователь должен иметь электронную почту')
        if not password or password == '': # проверка, что пароль передан и не пустой
            raise ValueError('Пользователь должен иметь пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) # создание объекта пользователя
        # TODO реализовать валидацию пароля
        user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') # хеширование пароля
        user.save(using=self._db) # сохранение пользователя в базе данных
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Функция создания суперпользователя
        """

        extra_fields.setdefault('is_staff', True) # указываем, что пользователь является сотрудником
        extra_fields.setdefault('is_superuser', True) # указываем, что пользователь является суперпользователем
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser):
    """
    Сущность пользователя
    """

    email = models.EmailField(unique=True) # если поле уникально, то оно индексируется автоматически
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True) # флаг для мягкого удаления пользователя
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager() # указываем, что менеджер для модели User - UserManager

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['first_name']

    def __str__(self):
        return self.email
    
    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    
    # так как в проекте не используется стандартная система разрешений Django,
    # то в реализации свойств и методов возвращаем False
    @property
    def is_staff(self):
        return False
    
    @property
    def is_superuser(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    def has_perm(self, perm, obj=None):
        return False
    
    def has_module_perms(self, app_label):
        return False