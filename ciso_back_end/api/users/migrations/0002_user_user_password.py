# Generated by Django 4.1 on 2022-09-13 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_password',
            field=models.CharField(default='Unknown', max_length=100, null=True),
        ),
    ]
