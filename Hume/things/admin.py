from django.contrib import admin
from .models import States, Districts, Things, ThingsReadings, Cluster
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


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('cluster_name', 'state', 'district', 'boundary')


@admin.register(Things)
class ThingsAdmin(admin.ModelAdmin):
    list_display = ('thing_type', 'collector', 'state', 'district', 'cluster', 'location_cordinate', 'is_active')


@admin.register(ThingsReadings)
class ThingsReadingsAdmin(admin.ModelAdmin):
    list_display = ('thing', 'reading_from', 'reading_till', 'rain_reading', 'temp_reading_min', 'temp_reading_max', 'created_at')