import json
from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from .serializers import InstanceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import *
from ..rightsizing_recommendation.services import *
from ..users.models import User
from ..users.serializers import UserSerializer
from ...commons.decorators.login_required import login_required
from ...commons.utils import decode_token


@api_view(['GET', 'POST'])
@login_required
def instance(request):
    if request.method == 'GET':
        instances = Instances.objects.all()
        instance_serializer = InstanceSerializer(instances, many=True)
        user_id = decode_token(request)["id"]

        for data in instance_serializer.data:
            cpu_usage_percentage, ram_usage_percentage, usage_category, recommendations, new_instance_family = get_usage_classifier(data["instance_name"], user_id)
            data["instance_status"] = usage_category

        return Response(instance_serializer.data)

    elif request.method == 'POST':
        aws_credentials = json.loads(str(request.body.decode('utf-8')).replace("'", '"'))

        user_id = decode_token(request)["id"]
        user = User.objects.get(user_id=user_id)
        user.user_aws_access_key = aws_credentials["access_key"]
        user.user_aws_secret_key = aws_credentials["secret_key"]
        user.save()

        instances = collect_ec2_instances(aws_credentials["access_key"],
                                          aws_credentials["secret_key"],
                                          user)

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@login_required
def instance_by_id(request, instance_id):
    if request.method == 'GET':
        user_id = decode_token(request)["id"]
        instances = get_object_or_404(Instances, pk=instance_id)
        usage_classifier_result = get_usage_classifier(instances.instance_name, user_id)
        instances.instance_status = usage_classifier_result[2]
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
