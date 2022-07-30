# Generated by Django 4.0.4 on 2022-05-13 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NodeBootTimeSeconds',
            fields=[
                ('time', models.DateTimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
                ('series_id', models.BigIntegerField(blank=True, null=True)),
                ('labels', models.TextField()),
                ('instance_id', models.IntegerField(primary_key=True, serialize=False)),
                ('job_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'node_boot_time_seconds',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NodeCpuSecondsTotal',
            fields=[
                ('time', models.DateTimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
                ('series_id', models.BigIntegerField(blank=True, null=True)),
                ('labels', models.TextField()),
                ('cpu_id', models.IntegerField(blank=True, null=True)),
                ('instance_id', models.IntegerField(primary_key=True, serialize=False)),
                ('job_id', models.IntegerField(blank=True, null=True)),
                ('mode_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'node_cpu_seconds_total',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NodeMemoryMemavailableBytes',
            fields=[
                ('time', models.DateTimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
                ('series_id', models.BigIntegerField(blank=True, null=True)),
                ('labels', models.TextField()),
                ('instance_id', models.IntegerField(primary_key=True, serialize=False)),
                ('job_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'node_memory_MemAvailable_bytes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NodeMemoryMemtotalBytes',
            fields=[
                ('time', models.DateTimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
                ('series_id', models.BigIntegerField(blank=True, null=True)),
                ('labels', models.TextField()),
                ('instance_id', models.IntegerField(primary_key=True, serialize=False)),
                ('job_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'node_memory_MemTotal_bytes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NodeUnameInfo',
            fields=[
                ('time', models.DateTimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
                ('series_id', models.BigIntegerField(blank=True, null=True)),
                ('labels', models.TextField()),
                ('domainname_id', models.IntegerField(blank=True, null=True)),
                ('instance_id', models.IntegerField(primary_key=True, serialize=False)),
                ('job_id', models.IntegerField(blank=True, null=True)),
                ('machine_id', models.IntegerField(blank=True, null=True)),
                ('nodename_id', models.IntegerField(blank=True, null=True)),
                ('release_id', models.IntegerField(blank=True, null=True)),
                ('sysname_id', models.IntegerField(blank=True, null=True)),
                ('version_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'node_uname_info',
                'managed': False,
            },
        ),
    ]
