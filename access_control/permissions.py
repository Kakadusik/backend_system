from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated
from .utils import check_permission

class HasElementPermission(BasePermission):
    """
    Класс проверки доступа к элементу. Для действий над списком используется has_permission,
    для конкретного объекта — has_object_permission.
    """
    def __init__(self, element_name, action):
        self.element_name = element_name
        self.action = action

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        has_perm, all_flag = check_permission(request.user, self.element_name, self.action)
        if not has_perm:
            return False
        # сохраняем флаг в request для использования в queryset или объектной проверке
        request.all_flag = all_flag
        return True

    def has_object_permission(self, request, view, obj):
        if self.action in ['update', 'delete', 'read']:
            if request.all_flag:
                return True
            owner = getattr(obj, 'owner', None)
            return owner == request.user
        return False
    
class IsAdminRole(BasePermission):
    """
    Класс проверки роли админа
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_roles.filter(role__name='admin').exists()