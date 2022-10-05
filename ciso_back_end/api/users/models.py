from django.db import models

<<<<<<< HEAD
from ciso_back_end.api.instances.models import Instances

=======
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_username = models.CharField(max_length=100)
    user_firstname = models.CharField(max_length=100)
    user_lastname = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
<<<<<<< HEAD
    user_password = models.CharField(max_length=100, default="Unknown", null=True)
    instance = models.ForeignKey(Instances, related_name='instances', on_delete=models.CASCADE)
=======
    user_aws_secret_key = models.TextField(default=None, null=True)
    user_aws_access_key = models.TextField(default=None, null=True)
    user_password = models.CharField(max_length=100, default="Unknown", null=True)
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
