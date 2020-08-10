"""
Data Admin
"""

from django.contrib import admin

from data import models


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_eui', 'status', 'owner', )
    list_filter = ('status', 'owner', )


@admin.register(models.Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('device', 'temperature', 'humidity', 'date', )
    list_filter = ('device', )
