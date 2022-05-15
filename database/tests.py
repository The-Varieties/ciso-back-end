import json
from time import sleep
from .models import *
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import factory

from .factory import InstancesFactory
from django.urls import reverse

PUBLIC_IPV4_ADDRESS = ['184.73.105.44:9100', '34.226.184.0:9100']

        
class RightSizingUtils(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.instance_objects = []
        
        for ipv4 in PUBLIC_IPV4_ADDRESS:
            self.instance_objects.append(InstancesFactory.build(
                                                        instance_ipv4=ipv4,
                                                        instance_AWSSecretKey="8ZIf4OUN2Btk8a4YitI+9RZArNITaQk2aP6Uct0N",
                                                        instance_AWSAccessKey="ASIATA5QGSDNK36XK5VS",
                                                        instance_AWSSessionToken="FwoGZXIvYXdzEMT//////////wEaDML6zGpRdwATazcG9yLEAQOqdFWNOFA/sRinHHOIHvAWAap8C+kfKC2d9ic1xQgkppMuRayKazoVB2/TqnhQ0P5dzZc7lMCbBHN0Iwy9xDDzpohogM2clZYcNfMiruN/rJEtKEaXdotO8TYVlNf80azZwAij3Z79dxrz+XotLE+aooxP+7YwwzOKbMPqr1y/c/ov5Ap1yisxhrPcl2jJVQr+/UnW54BdBYxoygXR/R+lrA8kPeVTqjzDmE95BPo78F7efvMtmTUR3k9n5RLmi/jdSSIo97qDlAYyLeViwmMr9mOjRgbK+VnSwwrZmrg25Qcx1kaHddZ1Tp3LOCn+MfV+3leYAC7YyQ=="))

        
        return super().setUp()
    
    def test_add_instances(self):
        data_dict = {
            "secret_key": self.instance_objects[0].instance_AWSSecretKey,
            "access_key": self.instance_objects[0].instance_AWSAccessKey,
            "session_token": self.instance_objects[0].instance_AWSSessionToken
        }
        
        response = self.client.post(reverse('instance'), data=data_dict, content_type=json)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        all_instances = Instance.objects.all()
        
        for i in range(len(all_instances)):
            self.assertEqual(self.instance_objects[i].instance_ipv4, all_instances[i].instance_ipv4)
        

        
    def test_delete_instances(self):
        data_dict = {
            "secret_key": self.instance_objects[0].instance_AWSSecretKey,
            "access_key": self.instance_objects[0].instance_AWSAccessKey,
            "session_token": self.instance_objects[0].instance_AWSSessionToken
        }
        
        self.client.post(reverse('instance'), data=data_dict, content_type=json)
        
        all_instances = Instance.objects.all()
        
        for i in range(len(all_instances)):
            response = self.client.delete(reverse('instance_by_id', kwargs={'id': all_instances[i].instance_id}))
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
        
        
        
   
            
        