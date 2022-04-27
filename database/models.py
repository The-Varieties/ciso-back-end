from django.db import models

class Instance(models.Model):
    instance_id = models.AutoField(primary_key=True)
    instance_name = models.CharField(max_length=100, unique=True)
    instance_status = models.CharField(max_length=100, null=True, default="Unknown")
    instance_ipv4 = models.CharField(max_length=100, unique=True)
    instance_AWSSecretKey = models.TextField(default="Unknown")
    instance_AWSAccessKey = models.TextField(default="Unknown")