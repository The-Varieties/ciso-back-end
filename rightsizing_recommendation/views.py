from ctypes import util
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from . import utils


@api_view(['GET'])
def get_cpu_usage(request):
    if request.method == 'GET':
        response_data = {
            'cpu': utils.get_cpu_usage( 
                request.query_params['time_interval'], 
                request.query_params['instance'])
        }
        return JsonResponse(response_data)

@api_view(['GET'])
def get_ram_usage(request):
    if request.method == 'GET':
        response_data = {
            'ram': utils.get_ram_usage(
                request.query_params['time_interval'],
                request.query_params['instance'])
        }
        return JsonResponse(response_data)
    
@api_view(['GET'])
def get_server_info(request):
    if request.method == 'GET':
        response_data = {
            'server_info': utils.get_server_info(
                request.query_params['instance']
            )
        }
        return JsonResponse(response_data)

