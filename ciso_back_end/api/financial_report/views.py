from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import *
from ...commons.decorators.login_required import login_required
from ...commons.utils import decode_token


@api_view(['GET'])
@login_required
def get_financial_report_all(request):
    user_id = decode_token(request)["id"]
    total_current_monthly_price, total_optimized_monthly_price, total_potential_savings, list_all_instances_cost = calculate_financial_report(
        user_id)
    response_data = {
        "total_current_monthly_price": total_current_monthly_price,
        "total_optimized_montly_price": total_optimized_monthly_price,
        "total_potential_savings": total_potential_savings,
        "data": list_all_instances_cost
    }
    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@login_required
def get_financial_report_single_instance(request):
    user_id = decode_token(request)["id"]
    current_hourly_price, current_monthly_price, optimized_hourly_price, optimized_monthly_price, potential_savings = calculate_single_instance_financial_report(
        request.query_params['instance_id'], user_id)

    response_data = {
        "current_hourly_price": current_hourly_price,
        "current_monthly_price": current_monthly_price,
        "optimized_hourly_price": optimized_hourly_price,
        "optimized_monthly_price": optimized_monthly_price,
        "potential_savings": potential_savings
    }
    return Response(data=response_data, status=status.HTTP_200_OK)
