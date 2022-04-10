from ctypes import util
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from . import utils


@api_view(['GET'])
def get_all(request):
    if request.method == 'GET':
        response_data = {
            'cpu': utils.get_cpu_usage()
        }
        return JsonResponse(response_data)
