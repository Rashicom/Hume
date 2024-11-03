from django import forms
from .models import ThingsReadings


class ReadingsForm(forms.ModelForm):
    class Meta:
        model = ThingsReadings
        fields = ["thing","reading_from", "reading_till","rain_reading", "temp_reading"]
    def clean_rain_reading(self):
        rain_reading = self.cleaned_data.get("rain_reading")
        if rain_reading < 0:
            raise forms.ValidationError("Rain reading cannot be negative.")
        return rain_reading
    def clean_temp_reading(self):
        temp_reading = self.cleaned_data.get("temp_reading")
        if temp_reading < 0 or temp_reading > 60:
            raise forms.ValidationError("Unexpected temperature reading")
        return temp_reading
    def clean(self):
        cleaned_data = super().clean()
        reading_from = cleaned_data.get("reading_from")
        reading_till = cleaned_data.get("reading_till")
        if reading_from > reading_till:
            self.add_error("reading_from", "Start date cannot be after end date.")
            self.add_error("reading_till", "End date cannot be before start date.")