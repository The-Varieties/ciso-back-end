from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import *
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

