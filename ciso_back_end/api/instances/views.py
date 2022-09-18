import json
from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from .serializers import InstanceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import *
from ..rightsizing_recommendation.services import *


@api_view(['GET', 'POST'])
def instance(request):
    if request.method == 'GET':
        instances = Instances.objects.all()
        instance_serializer = InstanceSerializer(instances, many=True)

        for data in instance_serializer.data:
            usage = get_usage_classifier(data["instance_name"])

            if usage:
                data["instance_status"] = usage
            else:
                data["instance_status"] = "Pending"

        return Response(instance_serializer.data)


    elif request.method == 'POST':
        aws_credentials = json.loads(str(request.body.decode('utf-8')).replace("'", '"'))

        instances = collect_ec2_instances(aws_credentials["access_key"],
                                          aws_credentials["secret_key"])

        is_many = isinstance(instances, list)
        instance_serializer = InstanceSerializer(data=instances, many=is_many)

        if not instance_serializer.is_valid():
            raise BadRequest(instance_serializer.errors)

        instance_serializer.save()

        return Response(data=instance_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
def instance_by_id(request, instance_id):
    if request.method == 'GET':
        instances = get_object_or_404(Instances, pk=instance_id)
        instances.instance_status = get_usage_classifier(instances.instance_name)[2]
        instance_serializer = InstanceSerializer(instances)

        return Response(data=instance_serializer.data)

    elif request.method == 'DELETE':
        instances = get_object_or_404(Instances, pk=instance_id)
        instances.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def sync_prometheus(request):
    if request.method == 'GET':
        response_data = get_targets_for_prometheus()
        return Response(response_data)
