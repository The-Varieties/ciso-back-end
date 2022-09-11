from login.models import Login
from rest_framework import viewsets, permissions
from .serializers import LoginSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    queryset = Login.objects.all()
    permission_classes = [permissions.AllowAny]