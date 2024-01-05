from django.contrib import admin

from .models import shelter

@admin.register(shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('id', 'location')

