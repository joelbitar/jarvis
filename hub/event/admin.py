# Register your models here.
from django.contrib import admin
from event.models import Sender, Signal

@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    pass

@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    pass
