from django.db import models
from accounts.models import User

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True) # индексируется на уровне бд
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class BusinessElement(models.Model):
    name = models.CharField(max_length=100, unique=True)  # например, 'product', 'order'
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='rules')
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE, related_name='rules')
    can_read = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'element')

    def __str__(self):
        return f"{self.role.name} - {self.element.name}"

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"