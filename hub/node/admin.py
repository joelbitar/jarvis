# Register your models here.
from django.contrib import admin
from node.models import Node, RequestLog

@admin.register(Node)
class SenderAdmin(admin.ModelAdmin):
    pass

@admin.register(RequestLog)
class SenderAdmin(admin.ModelAdmin):
    pass
