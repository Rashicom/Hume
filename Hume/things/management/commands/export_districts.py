import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from things.models import States, Districts

class Command(BaseCommand):
    help = "Export districts from a GeoJSON file"

    def add_arguments(self, parser):
        parser.add_argument('geojson_file', type=str, help="Path to the GeoJSON file")
        