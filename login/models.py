from django.db import models

# Create your models here.
class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    login_username = models.CharField(max_length=100)
    login_password = models.CharField(max_length=100)