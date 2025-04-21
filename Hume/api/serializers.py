from things.models import Things, ThingsReadings
from rest_framework import serializers

class ThingsReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThingsReadings
        fields = "__all__"
        read_only_fields = ["uuid", "thing", "created_at", "updated_at"]

    
    