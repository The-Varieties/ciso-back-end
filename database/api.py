from database.models import Instance
from rest_framework import viewsets, permissions
from .serializers import InstanceSerializer

class InstanceViewSet(viewsets.ModelViewSet):
    serializer_class = InstanceSerializer
    queryset = Instance.objects.all()
    permission_classes = [permissions.AllowAny]
