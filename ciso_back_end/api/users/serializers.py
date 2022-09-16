from ciso_back_end.api.users.models import User
from rest_framework import serializers
from ciso_back_end.api.instances.serializers import InstanceSerializer

class UserSerializer(serializers.ModelSerializer):
    instances = InstanceSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('user_id',
                  'user_username',
                  'user_firstname',
                  'user_lastname',
                  'user_email',
                  'user_password',
                  'instances')
