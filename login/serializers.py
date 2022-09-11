from login.models import Login
from rest_framework import serializers


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ('login_id', 'login_username', 'login_password')