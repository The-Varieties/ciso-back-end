from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from utils import utils


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def userApi(request,id=0):
    if request.method=='GET':
        user = User.objects.all()
        user_serializer = UserSerializer(user,many=True)
            
        return JsonResponse(user_serializer.data,safe=False)
    
    elif request.method=='POST':
        # instance_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method=='DELETE':
        user = get_object_or_404(User, pk=id)
        user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def syncPrometheus2(request):
    if request.method == 'GET':
        response_data = utils.get_targets_for_prometheus()
        return JsonResponse(response_data, safe=False)