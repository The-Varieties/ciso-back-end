from register.models import Register
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('register_id', 'register_username', 'register_firstname', 'register_lastname', 'register_email', 'register_password')
