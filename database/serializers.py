from database.models import Instance
from rest_framework import serializers


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ('instance_id', 'instance_name', 'instance_status', 'instance_ipv4', 'instance_AWSSecretKey', 'instance_AWSAccessKey')
