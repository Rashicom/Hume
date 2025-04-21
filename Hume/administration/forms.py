from django import forms
from things.models import States, Districts, Panjayath, Ward, Location

class StateForm(forms.ModelForm):
    class Meta:
        model = States
        fields = ['state_name']


class DistrictForm(forms.ModelForm):
    class Meta:
        model = Districts
        fields = ['district_name', 'state', 'boundary']

        