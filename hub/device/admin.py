# Register your models here.
from django.contrib import admin
from device.models import Device, DeviceGroup, Room, Placement

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'room', 'placement')

@admin.register(DeviceGroup)
class DeviceGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    pass