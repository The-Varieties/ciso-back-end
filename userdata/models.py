from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_username = models.CharField(max_length=100)
    user_firstname = models.CharField(max_length=100)
    user_lastname = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=100)
    user_city = models.CharField(max_length=100)