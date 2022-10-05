from django.db import models

<<<<<<< HEAD
=======
from ciso_back_end.api.users.models import User

>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516

class Instances(models.Model):
    instance_id = models.AutoField(primary_key=True)
    instance_name = models.CharField(max_length=100, unique=True)
    instance_status = models.CharField(max_length=100, null=True, default="Unknown")
    instance_ipv4 = models.CharField(max_length=100, unique=True)
<<<<<<< HEAD
    instance_aws_secret_key = models.TextField()
    instance_aws_access_key = models.TextField()
=======
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
    instance_region = models.TextField()
    instance_os = models.TextField(null=True)
    instance_volume_type = models.TextField(null=True)
    instance_type = models.TextField(null=True)
    instance_pricing_plan = models.TextField(null=True)
<<<<<<< HEAD
=======
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
>>>>>>> d4df3f2c7dd4f3be23c0f9f71570d4af88032516
