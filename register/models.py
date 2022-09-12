from django.db import models

# Create your models here.
from django.db import models

class Register(models.Model):
    register_id = models.AutoField(primary_key=True)
    register_username = models.CharField(max_length=100)
    register_firstname = models.CharField(max_length=100)
    register_lastname = models.CharField(max_length=100)
    register_email = models.CharField(max_length=100)
    register_password = models.CharField(max_length=100)