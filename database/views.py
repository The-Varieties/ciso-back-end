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
def instanceApi(request,id=0):
    if request.method=='GET':
        instance = Instance.objects.all()
        instance_serializer = InstanceSerializer(instance,many=True)
        
        for data in instance_serializer.data:
            data["instance_status"] = utils.get_usage_classifier(data["instance_name"])
            
        return JsonResponse(instance_serializer.data,safe=False)
    
    elif request.method=='POST':
        aws_credentials = request.POST.dict()
        # print(aws_credentials["secret_key"])
        
        instances = utils.collect_EC2_instances(aws_credentials["access_key"], 
                                    aws_credentials["secret_key"],
                                    aws_credentials["session_token"])
        
        is_many = isinstance(instances, list)
        
        instance_serializer = InstanceSerializer(data=instances, many=is_many)
        
        if not instance_serializer.is_valid(): 
            return Response(instance_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        instance_serializer.save()
        
        # mydata = json.loads(request.body.decode("utf-8"))
        # print(mydata["instance_name"])
        
        return Response(data=instance_serializer.data, status=status.HTTP_201_CREATED)
        
        # instance_serializer = InstanceSerializer(data=request.data)
        
        # if instance_serializer.is_valid():
        #     instance_serializer.save()
        #     return Response(data=instance_serializer.data, status=status.HTTP_201_CREATED)
        # return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method=='DELETE':
        instance = get_object_or_404(Instance, pk=id)
        instance.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    
# "ec2-44-204-214-30.compute-1.amazonaws.com:9100"
@api_view(['GET'])
def syncPrometheus(request):
    if request.method == 'GET':
        response_data = utils.get_targets_for_prometheus()
        return JsonResponse(response_data, safe=False)
