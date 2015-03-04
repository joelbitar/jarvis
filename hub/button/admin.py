# Register your models here.
from django.contrib import admin
from button.models import Button, ButtonLog

@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    pass

@admin.register(ButtonLog)
class ButtonLogAdmin(admin.ModelAdmin):
    pass
