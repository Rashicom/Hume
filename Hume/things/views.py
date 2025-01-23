from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReadingsForm
from django.utils import timezone
from .models import Things, ThingsReadings, States, Districts, Panjayath, Ward, Location
from django.http import JsonResponse
from datetime import datetime
from .utils import len_to_mm, temp_to_degree

class AddReadings(LoginRequiredMixin,View):
    """
    Add rain and temperature readings
    """
    def post(self, request):
        
        # fetch assigned thing
        thing = Things.objects.filter(collector=request.user).last()
        if not thing:
            print("No things mapping found")
            return render(request, 'collector_account.html', {"error":"Things Mapping not found"})

        # convert to base unit if unit is not in the base unit
        rain_unit = request.POST.get('rain_unit')
        temp_unit = request.POST.get('temp_unit')
        rain_reading = request.POST.get('rain_reading')
        temp_reading = request.POST.get('temp_reading')

        # covert to standard reading
        rain_standard_readings = len_to_mm(rain_unit, rain_reading)
        temp_standard_readings = temp_to_degree(temp_unit, temp_reading)

        # Date
        reading_from = request.POST.get('reading_from')
        reading_till = request.POST.get('reading_till')

        reading_from_utc = timezone.make_aware(datetime.strptime(reading_from, "%Y-%m-%dT%H:%M"), timezone.get_current_timezone())
        reading_till_utc = timezone.make_aware(datetime.strptime(reading_till, "%Y-%m-%dT%H:%M"), timezone.get_current_timezone())
        print("reading_from", reading_from_utc)
        print("reading_to", reading_till_utc)
        instance = ThingsReadings.objects.filter(thing=thing, created_at__date = timezone.now().date()).first()
        form = ReadingsForm(
            {
                "thing": thing,
                "reading_from": reading_from_utc,
                "reading_till":reading_till_utc,
                "rain_reading": rain_standard_readings,
                "temp_reading": temp_standard_readings,
            },
            instance=instance
        )
        if form.is_valid():
            form.save()
        else:
            return render(request, 'collector_account.html', {"form":form})
        return redirect("profile")


class LiveWeather(View):
    """
    render all live weather data with data
    """
    def get(self, request):
        return render(request,"liveweather.html")


class Test(View):
    def get(self, request):
        rd = ThingsReadings.objects.all().last()
        print("created_at:", rd.created_at.time())
        print("updated_at:", rd.updated_at)
        print("from :", rd.reading_from)
        print("till :", rd.reading_till)
        return render(request,"tt.html", {"date":rd})



class RainPatternView(View):
    def get(self, request):
        divition = request.queryparams.get("location_type")
        divition_value = request.queryparams.get("location_value")
        map_type = request.queryparams.get("map_type")
        

        return render(request,"rain_pattern.html")



