from datetime import datetime, timedelta

import boto3
import json
import calendar

from pkg_resources import resource_filename

from ciso_back_end.api.instances.models import Instances
from ciso_back_end.api.instances.serializers import InstanceSerializer
from ciso_back_end.api.rightsizing_recommendation.services import get_usage_classifier
from ciso_back_end.api.users.models import User
from ciso_back_end.commons.constant import NUMBER_HOURS_IN_A_MONTH


def _get_region_name(region_code):
    default_region = 'US East (N. Virginia)'
    endpoint_file = resource_filename('botocore', 'data/endpoints.json')
    region_code.rstrip(region_code[-1])
    if not region_code[-1].isdigit():
        region_code = region_code.rstrip(region_code[-1])
    try:
        with open(endpoint_file, 'r') as f:
            data = json.load(f)
        return data['partitions'][0]['regions'][region_code]['description'].replace('Europe', 'EU')
    except IOError:
        return default_region


def _get_date_range():
    current_date = datetime.now()
    days_number_of_month = calendar.monthrange(current_date.year, current_date.month)[1]
    return current_date.replace(day=1).date().__str__(), current_date.replace(day=days_number_of_month).date().__str__()


def get_ec2_instance_hourly_price(region_code,
                                  instance_type,
                                  user_id,
                                  operating_system='Linux',
                                  preinstalled_software='NA',
                                  tenancy='Shared',
                                  is_byol=False):
    region_name = _get_region_name(region_code)

    if is_byol:
        license_model = 'Bring your own license'
    else:
        license_model = 'No License required'

    if tenancy == 'Host':
        capacity_status = 'AllocatedHost'
    else:
        capacity_status = 'Used'

    filters = [
        {'Type': 'TERM_MATCH', 'Field': 'termType', 'Value': 'OnDemand'},
        {'Type': 'TERM_MATCH', 'Field': 'capacitystatus', 'Value': capacity_status},
        {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region_name},
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
        {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': tenancy},
        {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': operating_system},
        {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': preinstalled_software},
        {'Type': 'TERM_MATCH', 'Field': 'licenseModel', 'Value': license_model},
    ]

    user = User.objects.get(user_id=user_id)

    pricing_client = boto3.client(aws_access_key_id=user.user_aws_access_key,
                                  aws_secret_access_key=user.user_aws_secret_key,
                                  service_name='pricing',
                                  region_name='us-east-1')

    response = pricing_client.get_products(ServiceCode='AmazonEC2', Filters=filters)
    price_value = 0

    for price in response['PriceList']:
        price = json.loads(price)

        for on_demand in price['terms']['OnDemand'].values():
            for price_dimensions in on_demand['priceDimensions'].values():
                price_value = price_dimensions['pricePerUnit']['USD']

        return float(price_value)
    return None


def calculate_financial_report(user_id):
    instances = Instances.objects.raw(
        "SELECT * FROM instances_instances"
    )
    total_current_monthly_price = 0
    total_optimized_monthly_price = 0
    total_potential_savings = 0
    list_all_instances_cost = []

    for single_instance in instances:
        instance_serializer = InstanceSerializer(single_instance)
        current_hourly_price, current_monthly_price, optimized_hourly_price, optimized_monthly_price, potential_savings = calculate_savings(
            single_instance, user_id)
        temp_data_dict = {
            "instance": instance_serializer.data,
            "current_hourly_price": current_hourly_price,
            "current_monthly_price": current_monthly_price,
            "optimized_hourly_price": optimized_hourly_price,
            "optimized_monthly_price": optimized_monthly_price,
            "potential_savings": potential_savings
        }
        list_all_instances_cost.append(temp_data_dict)
        total_current_monthly_price += current_monthly_price
        total_optimized_monthly_price += optimized_monthly_price
        total_potential_savings += potential_savings

    return total_current_monthly_price, total_optimized_monthly_price, total_potential_savings, list_all_instances_cost


def calculate_single_instance_financial_report(instance_id, user_id):
    instances = Instances.objects.raw(
        "SELECT * FROM instances_instances WHERE instance_aws_id='{0}' LIMIT 1".format(instance_id)
    )

    for single_instance in instances:
        return calculate_savings(single_instance, user_id)


def calculate_savings(single_instance, user_id):
    tier_family = single_instance.instance_type
    region = single_instance.instance_region
    current_hourly_price = get_ec2_instance_hourly_price(region_code=region, instance_type=tier_family,
                                                         operating_system="Linux", user_id=user_id)
    current_monthly_price = current_hourly_price * NUMBER_HOURS_IN_A_MONTH
    cpu_usage_percentage, ram_usage_percentage, usage_category, recommendations, new_instance_family = get_usage_classifier(
        instance=single_instance.instance_name, user_id=user_id
    )
    optimized_hourly_price = get_ec2_instance_hourly_price(region_code=region, instance_type=new_instance_family,
                                                           operating_system="Linux", user_id=user_id)
    optimized_monthly_price = optimized_hourly_price * NUMBER_HOURS_IN_A_MONTH
    potential_savings = current_monthly_price - optimized_monthly_price
    return current_hourly_price, current_monthly_price, optimized_hourly_price, optimized_monthly_price, potential_savings
