from common.models import BaseModel
from django.conf import settings
from django.contrib.gis.db import models


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
    
# panjayathas
class Panjayath(BaseModel):
    panjayath_name = models.CharField(max_length=100)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    boundary = models.PolygonField(srid=4326, blank=True, null=True)

    def __str__(self):
        return str(self.panjayath_name)
    
class Ward(BaseModel):
    ward_name = models.CharField(max_length=100)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    panjayath = models.ForeignKey(Panjayath, on_delete=models.CASCADE)
    boundary = models.PolygonField(srid=4326, blank=True, null=True)

    def __str__(self):
        return str(self.ward_name)
    
class Location(BaseModel):
    location_name = models.CharField(max_length=100)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    panjayath = models.ForeignKey(Panjayath, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    boundary = models.PolygonField(srid=4326, blank=True, null=True)

    def __str__(self):
        return str(self.location_name)
    
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
    panjayath = models.ForeignKey(Panjayath, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    location_cordinate = models.PointField(srid=4326)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(f"{self.collector}:{self.location}")

class ThingsReadings(BaseModel):
    thing = models.ForeignKey(Things, on_delete=models.CASCADE, related_name="readings")
    reading_from = models.DateTimeField()
    reading_till = models.DateTimeField()
    rain_reading = models.FloatField(blank=True, null=True)
    temp_reading = models.FloatField(blank=True, null=True)
    soil_temp_reading = models.FloatField(blank=True, null=True)
    soil_humidity_reading= models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return str(f"{self.thing}:{self.reading_from}")
    


# Rainfall
# Temp
# soil tempS
# river flow (flood level)

# cumulative rainfall
