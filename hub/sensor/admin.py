from django.contrib import admin
from sensor.models import Sensor, SensorLog, SensorHourly, SensorDaily

# Register your models here.
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("name", "temperature", "humidity", "room")
    pass

# Register your models here.
@admin.register(SensorLog)
class SensorLogAdmin(admin.ModelAdmin):
    list_display = ("sensor", "temperature", "humidity", "created")
    ordering = ('id',)


class SensorMeanAdminBase(admin.ModelAdmin):
    list_display = ("sensor", "temperature_avg", "temperature_min", "temperature_max", "humidity_avg", "humidity_min", "humidity_max", "valid_for")

@admin.register(SensorHourly)
class SensorHourlyAdmin(SensorMeanAdminBase):
    pass

@admin.register(SensorDaily)
class SensorHourlyAdmin(SensorMeanAdminBase):
    pass
