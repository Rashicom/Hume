from django import forms
from things.models import States, Districts, Ward, Location
from authorization.models import Account

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
        