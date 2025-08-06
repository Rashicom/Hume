from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import RegistrationForm, LoginForm, PrifileUpdate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account
from things.models import Things, ThingsReadings
from django.utils import timezone


# login pnage get and post
class Login(View):
    form = LoginForm
    def post(self, request):
        login_form = LoginForm(
            {
                "mobile_number": request.POST.get('mobile_number'),
                "password": request.POST.get('password'),
            }
        )
        if login_form.is_valid():
            mobile_number = login_form.cleaned_data.get("mobile_number")
            password = login_form.cleaned_data.get("password")
            user = authenticate(request, mobile_number=mobile_number, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")
            else:
                return render(request, 'login.html', {"form": login_form, "error":"Invalid mobile_number or password"})
        return render(request, 'login.html', {"form": login_form})
    def get(self, request):
        return render(request, 'login.html')
    
# logout
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')

# register user
class Register(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        reg_form = RegistrationForm(
            {
                "mobile_number": request.POST.get('mobile_number'),
                "email": request.POST.get('email'),
                "name": request.POST.get('name'),
                "password": request.POST.get('password'),
                "role": request.POST.get('role'),
            }
        )
        if not reg_form.is_valid():
            return render(request, 'register.html', {"form":reg_form})

        return render(request, 'login.html')


# collector account
class Profile(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        user = request.user
        if user.role != Account.UserRole.DATA_COLLECTOR:
            return render(request, 'user_account.html')

        # data to to show in profile
        my_thing = Things.objects.filter(collector=user).last()
        month_first = timezone.now().date().replace(day=1)
        if my_thing:
            readings = my_thing.readings.all()
            today_readings = readings.filter(created_at__date=timezone.now().date()).last()
            data_contribution = {
                "total_collected":len(readings),
                "collected_this_month":len(readings.filter(updated_at__date__gt=month_first)),
                "rain":today_readings.rain_reading if today_readings else 0,
                "temp":today_readings.temp_reading if today_readings else 0
            }
        else:
            data_contribution = {}
        
        return render(request, 'collector_account.html', {"user":user, "mything":my_thing, "data":data_contribution})
    

class EditAccount(LoginRequiredMixin, View):
    login_url = 'login'
    def post(self, request):
        form = PrifileUpdate(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect("profile")


class News(View):
    def get(self, request):
        return render(request, 'news.html')

    
class About(View):
    def get(self, request):
        return render(request, 'about.html')
    
class Contact(View):
    def get(self, request):
        return render(request, 'contact.html')
    
class RainPattern(View):
    def get(self, request):
        return render(request, 'rain.html')

class TemperaturePattern(View):
    def get(self, request):
        return render(request, 'temperature.html')

class Gallery(View):
    def get(self, request):
        return render(request, 'gallery.html')
    
class TestMap(View):
    def get(self, request):
        coordinates = [
            {'lat': 40.7128, 'lng': -74.0060},  # New York
            {'lat': 34.0522, 'lng': -118.2437},  # Los Angeles
            {'lat': 51.5074, 'lng': -0.1278},    # London
        ]

        context = {'coordinates': coordinates}
        return render(request, 'map.html')
    


class AdminLogin(View):
    form = LoginForm
    def get(self, request):
        return render(request, "admin_login.html")
    
    def post(self, request):
        login_form = LoginForm(
            {
                "mobile_number": request.POST.get('mobile_number'),
                "password": request.POST.get('password'),
            }
        )
        if login_form.is_valid():
            mobile_number = login_form.cleaned_data.get("mobile_number")
            password = login_form.cleaned_data.get("password")
            user = authenticate(request, mobile_number=mobile_number, password=password)
            if not user:
                return render(request, 'admin_login.html', {"form": login_form, "error":"Invalid mobile_number or password"})
            if user.role != Account.UserRole.ADMIN:
                return render(request, 'admin_login.html', {"form": login_form, "error":"Permission blocked"})
            if user is not None:
                login(request, user)
                return redirect("admin-dashboard")
            else:
                return render(request, 'admin_login.html', {"form": login_form, "error":"Invalid mobile_number or password"})
        return render(request, 'admin_login.html', {"form": login_form})

# admin login 
class AdminLogout(View):
    def get(self, request):
        logout(request)
        return redirect('admin_login')