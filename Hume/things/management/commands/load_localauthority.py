import json
import os
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from things.models import States, Districts
from django.conf import settings


class Command(BaseCommand):
    help = "Export local authority from a GeoJSON file"

    def handle(self, *args, **options):
        geojson_path = os.path.join(settings.BASE_DIR, 'static', 'geojson', 'localauthority.geojson')

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

            district_name = feature['properties'].get('DISTRICT')
            geometry = feature.get('geometry')

            if district_name and geometry:
                geom = GEOSGeometry(json.dumps(geometry), srid=4326)

                # get or create district
                try:
                    district = Districts.objects.get(
                        district_name__iexact=district_name,
                        state=state
                    )

                    # update boundary if already exist
                    district.boundary = geom
                    district.save()

                except Exception as e:
                    district = Districts.objects.create(
                        district_name=district_name,
                        state=state,
                        boundary = geom
                    )

                self.stdout.write(self.style.SUCCESS(f"Processed: {district_name}"))
        self.stdout.write(self.style.SUCCESS("All districts loaded successfully."))