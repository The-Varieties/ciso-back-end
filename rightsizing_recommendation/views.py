from ctypes import util
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from utils import utils


@api_view(['GET'])
def get_cpu_usage(request):
    if request.method == 'GET':
        response_data = {
            'cpu': "{:.2f}%".format(utils.get_cpu_usage_v2( 
                request.query_params['time_interval'], 
                request.query_params['instance']))
        }
        return JsonResponse(response_data)

@api_view(['GET'])
def get_ram_usage(request):
    if request.method == 'GET':
        response_data = {
            'ram': "{:.2f}%".format(utils.get_ram_usage_v2(
                request.query_params['time_interval'],
                request.query_params['instance']))
        }
        return JsonResponse(response_data)
    
@api_view(['GET'])
def get_server_info(request):
    if request.method == 'GET':
        response_data = {
            'server_info': utils.get_server_info(
                request.query_params['instance']
            ),
            'uptime': utils.fetch_instance_details_db(
                request.query_params['instance'],
                'uptime'
            ),
            'cpu_count': utils.fetch_instance_details_db(
                request.query_params['instance'],
                'cpu_count'
            ),
            'total_ram': "{0} GB".format(utils.fetch_instance_details_db(
                request.query_params['instance'],
                'total_ram'
            ))
        }
        return JsonResponse(response_data)


@api_view(['GET'])
def get_usage_classifier(request):
    if request.method == 'GET':
        cpu_usage, ram_usage, usage_cat, recommendations = utils.get_usage_classifier(request.query_params['instance'], request.query_params['time_interval'])
        response_data = {
            'cpu': cpu_usage,
            'ram': ram_usage,
            'usage_cat': usage_cat,
            'recommendations': recommendations
        }
        return JsonResponse(response_data)