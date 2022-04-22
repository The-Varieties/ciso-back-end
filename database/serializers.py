from database.models import Instance
from rest_framework import serializers


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ('Instanceid', 'Instancename', 'Instancestatus', 'Instanceipv4')
