from django.contrib import admin
from dames import models
# Register your models here.

@admin.register(models.Partie)
class BasicAdmin(admin.ModelAdmin):
    pass
