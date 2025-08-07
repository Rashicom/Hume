import csv
import json
import os
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from things.models import States, Districts, Cluster
from django.conf import settings
from authorization.models import Account
from things.models import Things


class Command(BaseCommand):
    help = "Export users csv file"

    def handle(self, *args, **options):
        # Assumes a csv file named `users.csv` in `static/csv/`
        # with columns: name, mobile_number, cluster_name, latitude, longitude
        csv_path = os.path.join(settings.BASE_DIR, 'users.csv')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_path}"))
            return

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            print(reader)
            for row in reader:
                # Create or get Account
                user, user_created = Account.objects.get_or_create(
                    mobile_number=row['mobile_number'],
                    defaults={'name': row['name'], 'role': Account.UserRole.DATA_COLLECTOR}
                )
                if user_created:
                    user.set_password(row['mobile_number'])
                    user.save()

                # Get cluster
                cluster = Cluster.objects.filter(cluster_name__iexact=row['cluster_name']).first()

                # get state and district object
                state_obj = States.objects.filter(state_name__iexact=row['state']).first()
                district_obj = Districts.objects.filter(district_name__iexact=row['district']).first()

                if not state_obj or not district_obj:
                    self.stdout.write(self.style.ERROR("State or District not found"))
                    continue

                if not cluster:
                    self.stdout.write(self.style.ERROR("Cluster not found"))
                    continue

                # Create Things
                if not Things.objects.filter(collector=user).exists():
                    lat_str, lon_str = row["cordinates"].split()
                    point = Point(float(lon_str.strip()), float(lat_str.strip()), srid=4326)
                    Things.objects.create(
                        collector=user,
                        cluster=cluster,
                        location_cordinate=point,
                        state = state_obj,
                        district = district_obj,
                    )
                    self.stdout.write(self.style.SUCCESS(f"Processed user: {row['name']}"))
                else:
                    self.stdout.write(self.style.ERROR(f"User already mapped to the thing"))
                    continue

        self.stdout.write(self.style.SUCCESS("All users loaded successfully."))