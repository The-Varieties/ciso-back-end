# Generated by Django 4.1.2 on 2022-10-14 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '0004_remove_instances_instance_aws_access_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instances',
            name='instance_aws_id',
            field=models.CharField(default='Unknown', max_length=100, unique=True),
        ),
    ]
