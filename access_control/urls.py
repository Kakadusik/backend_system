from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, BusinessElementViewSet, AccessRuleViewSet, UserRoleViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'elements', BusinessElementViewSet)
router.register(r'rules', AccessRuleViewSet)
router.register(r'user-roles', UserRoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]