# Register your models here.
from django.contrib import admin
from device.models import Device, DeviceGroup

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass

@admin.register(DeviceGroup)
class DeviceGroupAdmin(admin.ModelAdmin):
    pass
