from ctypes import util
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from utils import utils

@api_view(['GET'])
def get_data_vis(request):
    if request.method == 'GET':
        response_data = utils.data_visualization(request.query_params['instance'], request.query_params['time_interval'], request.query_params['metric'])
        if response_data:
            return JsonResponse(response_data)
        else:
            return JsonResponse({"results": "Pending"})
