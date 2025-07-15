from common.models import BaseModel
from django.conf import settings
from django.contrib.gis.db import models


# json
# https://github.com/geohacker/kerala/blob/master/geojsons

# States
class States(BaseModel):
    state_name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.state_name)
    
# districts
class Districts(BaseModel):
    district_name = models.CharField(max_length=50)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    boundary = models.PolygonField(srid=4326,blank=True, null=True)

    def __str__(self):
        return str(self.district_name)

# cluster is a geographical area within a district which is defined by hume
class Cluster(BaseModel):
    cluster_name = models.CharField(max_length=100)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    boundary = models.PolygonField(srid=4326, blank=True, null=True)

    def __str__(self):
        return str(self.cluster_name)

    
# things
class Things(BaseModel):
    class ThingsType(models.TextChoices):
        RAIN_GAUGE = "RAIN_GAUGE"
        TEMPERATURE_GAUGE = "TEMPERATURE_GAUGE"
        RAIN_TEMP_GAUGE = "RAIN_TEMP_GAUGE"
    thing_type = models.CharField(max_length=50, choices=ThingsType, default=ThingsType.RAIN_TEMP_GAUGE)
    
    # collector who is collecting the data from the thing
    collector = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="my_things"
    )
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, blank=True, null=True)
    location_cordinate = models.PointField(srid=4326)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(f"{self.collector}:{self.cluster}")

class ThingsReadings(BaseModel):
    thing = models.ForeignKey(Things, on_delete=models.CASCADE, related_name="readings")
    reading_from = models.DateTimeField()
    reading_till = models.DateTimeField()
    rain_reading = models.FloatField(blank=True, null=True)
    temp_reading_min = models.FloatField(blank=True, null=True)
    temp_reading_max = models.FloatField(blank=True, null=True)
    soil_temp_reading = models.FloatField(blank=True, null=True)
    soil_humidity_reading= models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return str(f"{self.thing}:{self.reading_from}")
    


# Rainfall
# Temp
# soil tempS
# river flow (flood level)

# cumulative rainfall
