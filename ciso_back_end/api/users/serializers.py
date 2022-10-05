from ciso_back_end.api.users.models import User
from rest_framework import serializers
<<<<<<< HEAD
from ciso_back_end.api.instances.serializers import InstanceSerializer

class UserSerializer(serializers.ModelSerializer):
    instances = InstanceSerializer(many=True, read_only=True)
=======


class UserSerializer(serializers.ModelSerializer):
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
    class Meta:
        model = User
        fields = ('user_id',
                  'user_username',
                  'user_firstname',
                  'user_lastname',
<<<<<<< HEAD
                  'user_email',
                  'user_password',
                  'instances')
=======
                  'user_aws_access_key',
                  'user_aws_secret_key',
                  'user_email',
                  'user_password')
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
