from django.db import models


class Instances(models.Model):
    instance_id = models.AutoField(primary_key=True)
    instance_name = models.CharField(max_length=100, unique=True)
    instance_status = models.CharField(max_length=100, null=True, default="Unknown")
    instance_ipv4 = models.CharField(max_length=100, unique=True)
    instance_aws_secret_key = models.TextField()
    instance_aws_access_key = models.TextField()
    instance_region = models.TextField()
    instance_os = models.TextField(null=True)
    instance_volume_type = models.TextField(null=True)
    instance_type = models.TextField(null=True)
    instance_pricing_plan = models.TextField(null=True)
