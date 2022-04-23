from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Instance
from .serializers import InstanceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def instanceApi(request,id=0):
    if request.method=='GET':
        instance = Instance.objects.all()
        instance_serializer = InstanceSerializer(instance,many=True)
        return JsonResponse(instance_serializer.data,safe=False)
    
    elif request.method=='POST':
        # instance_data = JSONParser().parse(request)
        instance_serializer = InstanceSerializer(data=request.data)
        
        if instance_serializer.is_valid():
            instance_serializer.save()
            return Response(data=instance_serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method=='DELETE':
        instance = get_object_or_404(Instance, pk=id)
        instance.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
