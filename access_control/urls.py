from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, BusinessElementViewSet, AccessRuleViewSet, UserRoleViewSet

router = DefaultRouter() # роутер автоматически генерирует стандартный набор маршрутов
router.register(r'roles', RoleViewSet) # генерируются все маршруты для всех HTTP-методов
router.register(r'elements', BusinessElementViewSet)
router.register(r'rules', AccessRuleViewSet)
router.register(r'user-roles', UserRoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]