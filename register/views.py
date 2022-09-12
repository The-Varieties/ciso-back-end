from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Register
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utils import utils


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def registerApi(request,id=0):
    if request.method=='GET':
        register = Register.objects.all()
        register_serializer = RegisterSerializer(register,many=True)
            
        return JsonResponse(register_serializer.data,safe=False)
    
    elif request.method=='POST':
        # instance_data = JSONParser().parse(request)
        register_serializer = RegisterSerializer(data=request.data)
        
        if register_serializer.is_valid():
            register_serializer.save()
            return Response(data=register_serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method=='DELETE':
        register = get_object_or_404(Register, pk=id)
        register.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def syncPrometheus2(request):
    if request.method == 'GET':
        response_data = utils.get_targets_for_prometheus()
        return JsonResponse(response_data, safe=False)