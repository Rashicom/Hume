from django.contrib import admin
from .models import States, Districts, LocalAuthority, Ward, Location, Things, ThingsReadings
from django.utils.html import format_html


@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    list_display = ('state_name',)

@admin.register(Districts)
class DistrictsAdmin(admin.ModelAdmin):
    list_display = ('district_name', 'state', 'short_boundary')
    def short_boundary(self, obj):
        if obj.boundary:
            return format_html("Polygon with {} coords", len(obj.boundary.coords[0]))
        return "No boundary"

    short_boundary.short_description = "Boundary"

@admin.register(LocalAuthority)
class LocalAuthorityAdmin(admin.ModelAdmin):
    list_display = ('authority_type', 'state', 'district', 'boundary')

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('ward_name', 'state', 'district', 'localauthority', 'boundary')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'state', 'district', 'localauthority', 'ward', 'boundary')


@admin.register(Things)
class ThingsAdmin(admin.ModelAdmin):
    list_display = ('thing_type', 'collector', 'state', 'district', 'localauthority', 'ward', 'location', 'location_cordinate', 'is_active')


@admin.register(ThingsReadings)
class ThingsReadingsAdmin(admin.ModelAdmin):
    list_display = ('thing', 'reading_from', 'reading_till', 'rain_reading', 'created_at', 'updated_at')