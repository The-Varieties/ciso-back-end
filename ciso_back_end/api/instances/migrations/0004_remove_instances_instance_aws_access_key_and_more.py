# Generated by Django 4.1 on 2022-09-21 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '0003_instances_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instances',
            name='instance_aws_access_key',
        ),
        migrations.RemoveField(
            model_name='instances',
            name='instance_aws_secret_key',
        ),
    ]
