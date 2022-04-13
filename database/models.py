from django.db import models

class Instance(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=100, unique=True)
    ipv4 = models.CharField(max_length=100, unique=True)
