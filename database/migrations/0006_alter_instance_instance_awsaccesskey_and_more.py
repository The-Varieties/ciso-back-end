# Generated by Django 4.0.3 on 2022-04-27 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_alter_instance_instance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='instance_AWSAccessKey',
            field=models.TextField(default='Unknown'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='instance_AWSSecretKey',
            field=models.TextField(default='Unknown'),
        ),
    ]