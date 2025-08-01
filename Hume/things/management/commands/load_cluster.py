import json
import os
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from things.models import States, Districts, Cluster
from django.conf import settings


class Command(BaseCommand):
    help = "Export districts from a GeoJSON file"

    def handle(self, *args, **options):
        geojson_path = os.path.join(settings.BASE_DIR, 'static', 'geojson', 'cluster.geojson')

        if not os.path.exists(geojson_path):
            self.stdout.write(self.style.ERROR(f"GeoJSON file not found at {geojson_path}"))
            return
        
        with open(geojson_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        features = data.get("features", [])

        for feature in features:

            # create or get state
            state_name = feature['properties'].get('ST_NM')
            try:
                state = States.objects.get(state_name__iexact=state_name)
            except States.DoesNotExist:
                state = States.objects.create(state_name=state_name)

        self.stdout.write(self.style.SUCCESS("All districts loaded successfully."))