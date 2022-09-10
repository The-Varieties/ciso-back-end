from ciso_back_end.api.instances.models import Instances
from rest_framework import serializers


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instances
        fields = ('instance_id', 
                  'instance_name', 
                  'instance_status', 
                  'instance_ipv4',
                  'instance_aws_secret_key',
                  'instance_aws_access_key',
                  'instance_region',
                  'instance_os',
                  'instance_volume_type',
                  'instance_type',
                  'instance_pricing_plan')
