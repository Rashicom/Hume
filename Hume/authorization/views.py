from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
# Create your views here.


class Home(View):
    def get(self, request):
        return render(request, 'index.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    
class News(View):
    def get(self, request):
        return render(request, 'news.html')
    
class Register(View):
    def get(self, request):
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
        return render(request, 'map.html', context)