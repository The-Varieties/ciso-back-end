from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import *
from rest_framework.exceptions import NotFound
from rest_framework import status


@api_view(['GET'])
def login_user(request):
    if request.method == 'GET':
<<<<<<< HEAD
        user_id_result = authentice_user(request.query_params['username'], request.query_params['password'])
        if user_id_result:
            return Response(data=user_id_result, status=status.HTTP_200_OK)
=======
        token = authenticate_user(request.query_params['username'], request.query_params['password'])
        if token:
            return Response(data=token, status=status.HTTP_200_OK)
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
        else:
            raise NotFound()


