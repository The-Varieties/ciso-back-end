from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import *
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
            else:
                return Response(request,"The username is already exist!")
        except Exception:
            raise bad_request(request, Exception)


