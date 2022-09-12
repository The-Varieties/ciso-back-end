from register.models import Register
from rest_framework import viewsets, permissions
from .serializers import RegisterSerializer

class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()
    permission_classes = [permissions.AllowAny]