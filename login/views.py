from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Login
from .serializers import LoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utils import utils


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def userApi(request,id=0):
    if request.method=='GET':
        login = Login.objects.all()
        login_serializer = LoginSerializer(login,many=True)
            
        return JsonResponse(login_serializer.data,safe=False)
    
    elif request.method=='POST':
        # instance_data = JSONParser().parse(request)
        login_serializer = LoginSerializer(data=request.data)
        
        if login_serializer.is_valid():
            login_serializer.save()
            return Response(data=login_serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method=='DELETE':
        login = get_object_or_404(Login, pk=id)
        login.delete()
        return Response(status=status.HTTP_202_ACCEPTED)