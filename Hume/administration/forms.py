from django import forms
from things.models import States, Districts
from authorization.models import Account
from things.models import Things, ThingsReadings
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
        fields = ['collector', 'thing_type', 'state', 'district', 'cluster', 'location_cordinate']


class ThingsReadingForm(forms.ModelForm):
    class Meta:
        model = ThingsReadings
        fields = "__all__"