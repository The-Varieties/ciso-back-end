# Generated by Django 4.1 on 2022-09-13 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instances',
            name='instance_aws_access_key',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='instances',
            name='instance_aws_secret_key',
            field=models.TextField(),
        ),
    ]
