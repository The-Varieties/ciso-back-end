from django.db import models

from ciso_back_end.api.users.models import User


class Instances(models.Model):
    instance_id = models.AutoField(primary_key=True)
    instance_aws_id = models.CharField(max_length=100, unique=True, default="Unknown")
    instance_name = models.CharField(max_length=100, unique=True)
    instance_status = models.CharField(max_length=100, null=True, default="Unknown")
    instance_ipv4 = models.CharField(max_length=100, unique=True)
    instance_region = models.TextField()
    instance_os = models.TextField(null=True)
    instance_volume_type = models.TextField(null=True)
    instance_type = models.TextField(null=True)
    instance_pricing_plan = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
