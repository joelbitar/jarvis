from django.contrib import admin
from action.models import Action, ActionButton, ActionSensor

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    pass

@admin.register(ActionButton)
class ActionButtonAdmin(admin.ModelAdmin):
    pass

@admin.register(ActionSensor)
class ActionSensorAdmin(admin.ModelAdmin):
    pass
