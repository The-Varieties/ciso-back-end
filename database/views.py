from urllib import response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Instance
from .serializers import InstanceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utils import utils
import json


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def instance(request):
    if request.method=='GET':
        instance = Instance.objects.all()
        instance_serializer = InstanceSerializer(instance,many=True)
        
        for data in instance_serializer.data:
            usage = utils.get_usage_classifier(data["instance_name"])
            
            if usage:
                data["instance_status"] = usage
            else:
                data["instance_status"] = "Pending"
            
        return JsonResponse(instance_serializer.data,safe=False)
    
    elif request.method=='POST':
        aws_credentials = json.loads(request.body.decode('utf-8'))
        
        instances = utils.collect_EC2_instances(aws_credentials["access_key"], 
                                    aws_credentials["secret_key"],
                                    aws_credentials["session_token"])
        
        is_many = isinstance(instances, list)
        
        instance_serializer = InstanceSerializer(data=instances, many=is_many)
        
        if not instance_serializer.is_valid(): 
            return Response(instance_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        instance_serializer.save()
        
        return Response(data=instance_serializer.data, status=status.HTTP_201_CREATED)

    
    
@api_view(['GET', 'DELETE'])
def instanceById(request, id):
    if request.method == 'GET':
        try:
            instance = Instance.objects.get(pk=id)
        except Instance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        instance_serializer = InstanceSerializer(instance)
        data = instance_serializer.data
        data["instance_status"] = utils.get_usage_classifier(data["instance_name"])

    
        return Response(instance_serializer.data, status=status.HTTP_200_OK)
        
    elif request.method=='DELETE':
        instance = get_object_or_404(Instance, pk=id)
        instance.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def syncPrometheus(request):
    if request.method == 'GET':
        response_data = utils.get_targets_for_prometheus()
        return JsonResponse(response_data, safe=False)
    

