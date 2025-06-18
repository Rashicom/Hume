from django import forms
from things.models import States, Districts, Ward, Location
from authorization.models import Account
from things.models import Things
from django.contrib.gis.geos import Point


class StateForm(forms.ModelForm):
    class Meta:
        model = States
        fields = ['state_name']


class DistrictForm(forms.ModelForm):
    class Meta:
        model = Districts
        fields = ['district_name', 'state', 'boundary']


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['name', 'mobile_number', 'email', 'role']
    

class ThingsRegistrationForm(forms.ModelForm):
    class Meta:
        model = Things
        fields = ['collector', 'thing_type', 'state', 'district', 'location_cordinate']
    
    def clean_location_cordinate(self):
        print(">>>>>>>>>")
        value = self.cleaned_data['location_cordinate']
        if isinstance(value, str):
            try:
                lat_str, lon_str = value.split(",")
                point = Point(float(lon_str.strip()), float(lat_str.strip()))  # Note: Point(x=lon, y=lat)
                return point
            except Exception:
                raise forms.ValidationError("Invalid format. Use 'latitude,longitude'")
        return value