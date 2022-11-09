from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import *
from ...commons.decorators.login_required import login_required
from ...commons.utils import decode_token


@api_view(['GET'])
@login_required
def get_cpu_usage(request):
    if request.method == 'GET':
        response_data = {
            'cpu': "{:.2f}%".format(get_cpu_usage_v2(
                request.query_params['time_interval'],
                request.query_params['instance']))
        }
        return Response(response_data)


@api_view(['GET'])
@login_required
def get_ram_usage(request):
    if request.method == 'GET':
        response_data = {
            'ram': "{:.2f}%".format(get_ram_usage_v2(
                request.query_params['instance']))
        }
        return Response(response_data)


@api_view(['GET'])
@login_required
def get_server_info(request):
    if request.method == 'GET':
        response_data = {
            'server_info': get_instance_server_info(
                request.query_params['instance']
            ),
            'uptime': get_instance_uptime(
                request.query_params['instance']
            ),
            'cpu_count': get_instance_cpu_count(
                request.query_params['instance']
            ),
            'total_ram': "{0} GB".format(get_instance_total_ram(
                request.query_params['instance']
            ))
        }
        return Response(response_data)


@api_view(['GET'])
@login_required
def get_usage_category(request):
    if request.method == 'GET':
        user_id = decode_token(request)["id"]
        usage_classifier_result = get_usage_classifier(request.query_params['instance'], user_id, request.query_params['time_interval'])
        response_data = {
            'cpu': usage_classifier_result[0] if usage_classifier_result[0] else '',
            'ram': usage_classifier_result[1] if usage_classifier_result[1] else '',
            'usage_cat': usage_classifier_result[2],
            'recommendations': usage_classifier_result[3],
            'recommended_instance_family': usage_classifier_result[4],
        }
        return Response(response_data)
