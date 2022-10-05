from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import *
<<<<<<< HEAD
from rest_framework.exceptions import NotFound
from rest_framework import status


@api_view(['GET'])
def register_user(request):
    if request.method == 'GET':
        user_id_result = authentice_user(request.query_params['username'], request.query_params['password'])
        if user_id_result:
            return Response(data=user_id_result, status=status.HTTP_200_OK)
        else:
            raise NotFound()
=======
from rest_framework.exceptions import bad_request
from rest_framework import status

from ..users.serializers import UserSerializer


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        try:
            user_serializer = UserSerializer(data=request.data)

            if user_serializer.is_valid():
                user_serializer.save()
                return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            raise bad_request(request, Exception)

>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516

