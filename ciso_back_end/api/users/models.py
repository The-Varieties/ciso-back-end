from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_username = models.CharField(max_length=100)
    user_firstname = models.CharField(max_length=100)
    user_lastname = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_aws_secret_key = models.TextField(default=None, null=True)
    user_aws_access_key = models.TextField(default=None, null=True)
    user_password = models.CharField(max_length=100, default="Unknown", null=True)
