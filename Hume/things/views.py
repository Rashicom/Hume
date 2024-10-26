from django.shortcuts import render, redirect
from django.views import View


class AddReadings(View):
    """
    Add rain and temperature readings
    """
    def post(self, request):
        print("Add readings post request")
        return redirect("collector-account")