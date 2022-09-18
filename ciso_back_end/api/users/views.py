from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import User
from .serializers import UserSerializer


@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def user_api(request, user_id=0):
    if request.method == 'GET':
        user = User.objects.all()
        user_serializer = UserSerializer(user, many=True)

        return Response(user_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
        raise NotFound()

    elif request.method == 'DELETE':
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
