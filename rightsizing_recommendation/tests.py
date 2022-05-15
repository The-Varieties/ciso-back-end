from .models import *
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

        
# class RightSizingUtils(APITestCase):
#     def test_get_cpu_usage(self):
#         response = self.client.get(reverse('get-cpu-usage'), {"instance": "node_exporter", "time_interval": "5 minutes"})
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#     def test_get_ram_usage(self):
#         response = self.client.get(reverse('get-ram-usage'), {"instance": "node_exporter", "time_interval": "5 minutes"})
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#     def test_get_server_info(self):
#         response = self.client.get(reverse('get-server-info'), {"instance": "node_exporter"})
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#     def test_get_usage_category(self):
#         response = self.client.get(reverse('get-usage-category'), {"instance": "node_exporter", "time_interval": "5 minutes"})
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)