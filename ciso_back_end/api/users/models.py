from django.db import models

from ciso_back_end.api.instances.models import Instances


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_username = models.CharField(max_length=100)
    user_firstname = models.CharField(max_length=100)
    user_lastname = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100, default="Unknown", null=True)
    instance = models.ForeignKey(Instances, related_name='instances', on_delete=models.CASCADE)