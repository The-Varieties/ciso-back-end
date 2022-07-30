# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NodeCpuSecondsTotal(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    series_id = models.BigIntegerField(blank=True, null=True)
    labels = models.TextField()  # This field type is a guess.
    cpu_id = models.IntegerField(blank=True, null=True)
    instance_id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(blank=True, null=True)
    mode_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'node_cpu_seconds_total'


class NodeMemoryMemavailableBytes(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    series_id = models.BigIntegerField(blank=True, null=True)
    labels = models.TextField()  # This field type is a guess.
    instance_id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'node_memory_MemAvailable_bytes'


class NodeMemoryMemtotalBytes(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    series_id = models.BigIntegerField(blank=True, null=True)
    labels = models.TextField()  # This field type is a guess.
    instance_id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'node_memory_MemTotal_bytes'


class NodeBootTimeSeconds(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    series_id = models.BigIntegerField(blank=True, null=True)
    labels = models.TextField()  # This field type is a guess.
    instance_id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'node_boot_time_seconds'


class NodeUnameInfo(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    series_id = models.BigIntegerField(blank=True, null=True)
    labels = models.TextField()  # This field type is a guess.
    domainname_id = models.IntegerField(blank=True, null=True)
    instance_id = models.IntegerField(primary_key=True)
    job_id = models.IntegerField(blank=True, null=True)
    machine_id = models.IntegerField(blank=True, null=True)
    nodename_id = models.IntegerField(blank=True, null=True)
    release_id = models.IntegerField(blank=True, null=True)
    sysname_id = models.IntegerField(blank=True, null=True)
    version_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'node_uname_info'
