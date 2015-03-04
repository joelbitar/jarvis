from django.contrib import admin
from sensor.models import Sensor, SensorLog

# Register your models here.
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass

# Register your models here.
@admin.register(SensorLog)
class SensorLogAdmin(admin.ModelAdmin):
    pass


