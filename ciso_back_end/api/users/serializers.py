from ciso_back_end.api.users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id',
                  'user_username',
                  'user_firstname',
                  'user_lastname',
                  'user_email',
                  'user_password')
