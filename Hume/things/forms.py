from django import forms
from .models import ThingsReadings


class ReadingsForm(forms.ModelForm):
    class Meta:
        model = ThingsReadings
        fields = ["thing","reading_from", "reading_from","rain_reading", "temp_reading"]