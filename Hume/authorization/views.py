from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login
# Create your views here.


class Home(View):
    def get(self, request):
        return render(request, 'index.html')


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
                return render(request, 'login.html')    
            else:
                login_form.add_error("mobile_number", "Invalid mobile_number or password")
                return render(request, 'login.html', {"form": login_form})
        return render(request, 'login.html', {"form": login_form})
    def get(self, request):
        return render(request, 'login.html')
    
class News(View):
    def get(self, request):
        return render(request, 'news.html')
    
class Register(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        print("neme :", request.POST.get('mobile_number'))
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
            print(reg_form.errors)
            return render(request, 'register.html', {"form":reg_form})

        return render(request, 'register.html')
        

class Staff(View):
    def get(self, request):
        return render(request, 'staff.html')
    
class About(View):
    def get(self, request):
        return render(request, 'about.html')
    
class Contact(View):
    def get(self, request):
        return render(request, 'contact.html')
    
class Elements(View):
    def get(self, request):
        return render(request, 'elements.html')

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