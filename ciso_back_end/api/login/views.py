from os import stat
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import *
from rest_framework.exceptions import NotFound
from rest_framework import status


@api_view(['GET'])
def login_user(request):
    if request.method == 'GET':
        token = authenticate_user(request.query_params['username'], request.query_params['password'])
        if token:
            return Response(data=token, status=status.HTTP_200_OK)
        else:
            return Response(data=None, status=status.HTTP_200_OK)


