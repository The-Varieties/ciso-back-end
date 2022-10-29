from datetime import datetime, timedelta

import awspricing
import boto3
import json
from pkg_resources import resource_filename

FLT = '[{{"Field": "tenancy", "Value": "shared", "Type": "TERM_MATCH"}},' \
      '{{"Field": "operatingSystem", "Value": "{o}", "Type": "TERM_MATCH"}},' \
      '{{"Field": "preInstalledSw", "Value": "NA", "Type": "TERM_MATCH"}},' \
      '{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}},' \
      '{{"Field": "location", "Value": "{r}", "Type": "TERM_MATCH"}},' \
      '{{"Field": "capacitystatus", "Value": "Used", "Type": "TERM_MATCH"}}]'


def get_price(client, region, instance, os):
    f = FLT.format(r=region, t=instance, o=os)
    data = client.get_products(ServiceCode='AmazonEC2', Filters=json.loads(f))
    od = json.loads(data['PriceList'][0])['terms']['OnDemand']
    id1 = list(od)[0]
    id2 = list(od[id1]['priceDimensions'])[0]
    return od[id1]['priceDimensions'][id2]['pricePerUnit']['USD']


def _get_region_name(region_code):
    default_region = 'US East (N. Virginia)'
    endpoint_file = resource_filename('botocore', 'data/endpoints.json')
    try:
        with open(endpoint_file, 'r') as f:
            data = json.load(f)
        return data['partitions'][0]['regions'][region_code]['description'].replace('Europe', 'EU')
    except IOError:
        return default_region


def calculate_financial_report():
    client = boto3.client(aws_access_key_id="AKIA2Q5I3UYGG2ODJJDX",
                          aws_secret_access_key="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",
                          service_name='pricing',
                          region_name='us-east-1')

    current_cost_usage = fetch_current_cost()

    price = get_price(client, _get_region_name('eu-west-1'), 't3.micro', 'Linux')
    return current_cost_usage


def fetch_current_cost():
    today_date = datetime.today().date().__str__()
    last_month_date = datetime.today() - timedelta(days=30)
    last_month_date = last_month_date.date().__str__()
    client = boto3.client(aws_access_key_id="AKIA2Q5I3UYGG2ODJJDX",
                          aws_secret_access_key="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",
                          service_name='ce',
                          region_name='us-east-1')
    response = client.get_rightsizing_recommendation(
        Configuration={
            'RecommendationTarget': 'SAME_INSTANCE_FAMILY',
            'BenefitsConsidered': True
        },
        Service='AmazonEC2'
    )
    # EC2 - Other

    response2 = client.get_cost_and_usage(
        TimePeriod={
            'Start': last_month_date,
            'End': today_date
        },
        Granularity='MONTHLY',
        Metrics=[
            'UsageQuantity',
            'UnblendedCost'
        ],
        Filter={
            'Dimensions': {
                'Key': 'SERVICE',
                'Values': [
                    'Amazon Elastic Compute Cloud - Compute',
                    'EC2 - Other'
                ]
            }
        },
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )
    return response

def get_current_expenses():
    client = boto3.client('ce', region_name='us-east-1')

    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': '2018-10-01',
            'End': '2018-10-31'
        },
        Granularity='MONTHLY',
        Metrics=[
            'AmortizedCost',
        ]
    )

    print(response)
    return None

# def calculate_financial_report():
#     # awspricing.client = boto3.client(service_name='pricing',
#     #                                  aws_access_key_id="AKIA2Q5I3UYGG2ODJJDX",
#     #                                  aws_secret_access_key="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",
#     #                                  region_name='us-east-1')
#
#     ec2_offer = awspricing.offer('AmazonEC2')
#
#     hourly = ec2_offer.reserved_hourly(
#         'c4.xlarge',
#         operating_system='Linux',
#         lease_contract_length='3yr',
#         offering_class='convertible',
#         purchase_option='Partial Upfront',
#         region='us-east-1'
#     )
#
#     return hourly
