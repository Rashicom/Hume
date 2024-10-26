from django.contrib import admin
from .models import States, Districts, Panjayath, Ward, Location, Things, ThingsReadings

@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    list_display = ('state_name',)

@admin.register(Districts)
class DistrictsAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'state', 'boundary')

@admin.register(Panjayath)
class PanjayathAdmin(admin.ModelAdmin):
    list_display = ('panjayath_name', 'state', 'district', 'boundary')

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('ward_name', 'state', 'district', 'panjayath', 'boundary')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'state', 'district', 'panjayath', 'ward', 'boundary')


@admin.register(Things)
class ThingsAdmin(admin.ModelAdmin):
    list_display = ('thing_type', 'collector', 'state', 'district', 'panjayath', 'ward', 'location', 'location_cordinate', 'is_active')


@admin.register(ThingsReadings)
class ThingsReadingsAdmin(admin.ModelAdmin):
    list_display = ('thing', 'reading_from', 'reading_till', 'rain_reading', 'temp_reading')