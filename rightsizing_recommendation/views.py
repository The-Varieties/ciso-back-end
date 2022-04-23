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
            'cpu': "{:.2f}%".format(utils.get_cpu_usage( 
                request.query_params['time_interval'], 
                request.query_params['instance']))
        }
        return JsonResponse(response_data)

@api_view(['GET'])
def get_ram_usage(request):
    if request.method == 'GET':
        response_data = {
            'ram': "{:.2f}%".format(utils.get_ram_usage(
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
        response_data = {
            'usage_cat': utils.get_usage_classifier(
                request.query_params['instance']
            )
        }
        return JsonResponse(response_data)

@api_view(['GET'])
def get_rx(request):
    if request.method == 'GET':
        response_data = [{
            "targets": ["node-exporter:9100", "ec2-44-204-214-30.compute-1.amazonaws.com:9100"],
            "labels": {
                "hostname": "node"
            }
        }]
        return JsonResponse(response_data, safe=False)