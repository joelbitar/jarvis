from django.contrib import admin
from forecast.models import Forecast

@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    pass

