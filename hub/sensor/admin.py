from django.contrib import admin
from sensor.models import Sensor, SensorLog, SensorHourly, SensorDaily

# Register your models here.
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass

# Register your models here.
@admin.register(SensorLog)
class SensorLogAdmin(admin.ModelAdmin):
    pass

@admin.register(SensorHourly)
class SensorHourlyAdmin(admin.ModelAdmin):
    pass

@admin.register(SensorDaily)
class SensorHourlyAdmin(admin.ModelAdmin):
    pass
