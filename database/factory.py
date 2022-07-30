import factory
from .models import *



REGIONS = ['us-east-1', 'us-east-2', 'us-east-3']
INSTANCE_TYPE = ['t2.micro', 't2.small']

class InstancesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Instance
        
    instance_name = factory.Faker('name')
    instance_status = "Unknown"
    instance_ipv4 = "Unknown"
    instance_AWSSecretKey = "Unknown"
    instance_AWSAccessKey = "Unknown"
    instance_AWSSessionToken = "Unknown"
    instance_region = factory.Faker('random_element', elements=REGIONS)
    instance_os = "Linux/UNIX"
    instance_volume_type = "gp2"
    instance_type = factory.Faker('random_element', elements=INSTANCE_TYPE)
    instance_pricing_plan = "Reservation"