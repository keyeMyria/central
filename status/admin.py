from django.contrib import admin
from status.models import *
# Register your models here.

class Detail(admin.StackedInline):
    model = Detail
class Status(admin.TabularInline):
    model = Status

#@admin.register(Status)
#class StatusAdmin(admin.ModelAdmin):
#    list_display = ['ip', 'up', 'state', 'lastseen']
#    ordering = ['lastseen']
#    search_fields = ['dns', 'name']
#    list_filter = ['up', 'state']

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ['name', 'dns', 'ip', 'state', 'up', 'user']
    inlines = [Status, Detail]
    def up(self, obj):
        return bool(obj.status.up)
#@admin.register(Detail)
#class BasicAdmin(admin.ModelAdmin):
#    pass