from ciso_back_end.api.instances.models import Instances
from rest_framework import serializers

<<<<<<< HEAD

class InstanceSerializer(serializers.ModelSerializer):
=======
from ciso_back_end.api.users.models import User
from ciso_back_end.api.users.serializers import UserSerializer


class InstanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
    class Meta:
        model = Instances
        fields = ('instance_id', 
                  'instance_name', 
                  'instance_status', 
                  'instance_ipv4',
<<<<<<< HEAD
                  'instance_aws_secret_key',
                  'instance_aws_access_key',
=======
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
                  'instance_region',
                  'instance_os',
                  'instance_volume_type',
                  'instance_type',
<<<<<<< HEAD
                  'instance_pricing_plan')
=======
                  'instance_pricing_plan',
                  'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.get(pk=user_data['user_id'])
        instance = Instances.objects.create(**validated_data)
        User.objects.create(instance=instance, **user_data)
        return instance


>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
