from things.models import ThingsReadings, Cluster
from rest_framework import serializers

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = "__all__"

class ThingsReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThingsReadings
        fields = "__all__"
        read_only_fields = ["uuid", "thing", "created_at", "updated_at"]

    
class DailyAverageSerializer(serializers.Serializer):
    day = serializers.DateField()
    avg_rain = serializers.FloatField()
    avg_temp_min = serializers.FloatField()
    avg_temp_max = serializers.FloatField()
    avg_soil_temp = serializers.FloatField()
    avg_soil_humidity = serializers.FloatField()