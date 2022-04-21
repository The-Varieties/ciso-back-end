from django.test import TestCase
from .models import *
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

client = Client()

class RightSizingModels(TestCase):
    def test_node_cpu_tables_count(self):
        self.assertNotEqual(0, NodeCpuSecondsTotal.objects.count())

    def test_node_memory_available_count(self):
        self.assertNotEqual(0, NodeMemoryMemavailableBytes.objects.count())
    
    def test_mode_memory_total_count(self):
        self.assertNotEqual(0, NodeMemoryMemtotalBytes.objects.count())
        
    def test_boot_time_count(self):
        self.assertNotEqual(0, NodeBootTimeSeconds.objects.count())
        
    def test_node_uname_count(self):
        self.assertNotEqual(0, NodeUnameInfo.objects.count())
        
class RightSizingUtils(TestCase):
    def test_get_cpu_usage(self):
        response = client.get(reverse('get-cpu-usage'), {"instance": "node_exporter", "time_interval": "5 minutes"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_ram_usage(self):
        response = client.get(reverse('get-ram-usage'), {"instance": "node_exporter", "time_interval": "5 minutes"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_server_info(self):
        response = client.get(reverse('get-server-info'), {"instance": "node_exporter"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_usage_category(self):
        response = client.get(reverse('get-usage-category'), {"instance": "node_exporter", "time_interval": "5 minutes"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)