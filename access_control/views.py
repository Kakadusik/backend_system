from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Role, BusinessElement, AccessRule, UserRole
from .serializers import RoleSerializer, BusinessElementSerializer, AccessRuleSerializer, UserRoleSerializer
from .permissions import IsAdminRole

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

class BusinessElementViewSet(ModelViewSet):
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

class AccessRuleViewSet(ModelViewSet):
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

class UserRoleViewSet(ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]