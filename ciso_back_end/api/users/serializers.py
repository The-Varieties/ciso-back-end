from ciso_back_end.api.users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = User
        fields = ('user_id',
                  'user_username',
                  'user_firstname',
                  'user_lastname',
                  'user_aws_access_key',
                  'user_aws_secret_key',
                  'user_email',
                  'user_password')
