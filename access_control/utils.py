from .models import AccessRule

def check_permission(user, element_name, action):
    """
    Функция проверки разрешений пользователя, возвращает кортеж (has_perm, all_flag)
    """
    if not user.is_authenticated:
        return False, False

    # Получаем все роли пользователя
    user_roles = user.user_roles.values_list('role_id', flat=True)
    if not user_roles:
        return False, False

    # Ищем правило для любой из ролей (можно усложнить: объединять права из нескольких ролей)
    rule = AccessRule.objects.filter(
        role_id__in=user_roles,
        element__name=element_name
    ).first()
    if not rule:
        return False, False

    perm_map = {
        'read': ('can_read', 'can_read_all'),
        'create': ('can_create', None),
        'update': ('can_update', 'can_update_all'),
        'delete': ('can_delete', 'can_delete_all')
    }
    if action not in perm_map:
        return False, False

    base_perm, all_perm_field = perm_map[action]
    if not getattr(rule, base_perm):
        return False, False

    if all_perm_field:
        return True, getattr(rule, all_perm_field)
    else:
        return True, False  # для create all_flag не используется