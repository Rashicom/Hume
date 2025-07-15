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

class ThiresReadingsMapSerializer(serializers.ModelSerializer):
    cordinate = serializers.SerializerMethodField()
    class Meta:
        model = ThingsReadings
        fields = ["created_at", "thing", "cordinate", "rain_reading", "temp_reading_min", "temp_reading_max", "soil_temp_reading", "soil_humidity_reading"]
    
    def get_cordinate(self, obj):
        return obj.thing.location_cordinate.coords