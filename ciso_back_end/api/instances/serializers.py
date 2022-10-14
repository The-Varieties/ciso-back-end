from ciso_back_end.api.instances.models import Instances
from rest_framework import serializers

from ciso_back_end.api.users.models import User
from ciso_back_end.api.users.serializers import UserSerializer


class InstanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Instances
        fields = ('instance_id',
                  'instance_aws_id',
                  'instance_name', 
                  'instance_status', 
                  'instance_ipv4',
                  'instance_region',
                  'instance_os',
                  'instance_volume_type',
                  'instance_type',
                  'instance_pricing_plan',
                  'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        instance = Instances.objects.create(**validated_data)
        User.objects.create(instance=instance, **user_data)
        return instance


