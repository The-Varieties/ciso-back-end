from django.db import models

class Instance(models.Model):
    Instanceid = models.AutoField(primary_key=True)
    Instancename = models.CharField(max_length=100, unique=True)
    Instancestatus = models.CharField(max_length=100, unique=True, null=True, default="Unknown")
    Instanceipv4 = models.CharField(max_length=100, unique=True)
    InstanceAWSSecretKey = models.TextField(unique=True, default="Unknown")
    InstanceAWSAccessKey = models.TextField(unique=True, default="Unknown")