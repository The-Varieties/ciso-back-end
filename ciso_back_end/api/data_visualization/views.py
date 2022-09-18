from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import *


@api_view(['GET'])
def get_data_vis_cpu(request):
    response_data = {
        'name': 'CPU',
        'time': 'last %s' % request.query_params['time_interval']
    }
    hostname, results = get_data_visualization_cpu(
        request.query_params['instance'],
        request.query_params['time_interval'])

    response_data['hostname'] = hostname
    response_data['results'] = results

    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_data_vis_ram(request):
    response_data = {
        'name': 'RAM',
        'time': 'last %s' % request.query_params['time_interval']
    }

    hostname, results = get_data_visualization_ram(
        request.query_params['instance'],
        request.query_params['time_interval'])

    response_data['hostname'] = hostname
    response_data['results'] = results

    return Response(data=response_data, status=status.HTTP_200_OK)


