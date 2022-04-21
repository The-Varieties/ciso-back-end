from django.test import TestCase
from .models import *

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
        
# class RightSizingUtils(TestCase):
    