from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('news/', views.News.as_view(), name='news'),
    path('register/', views.Register.as_view(), name='register'),
    path('staff/', views.Staff.as_view(), name='staff'),
    path('about/', views.About.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('elements/', views.Elements.as_view(), name='elements'),
    path('gallery/', views.Gallery.as_view(), name='gallery'),

    path('map/', views.TestMap.as_view(), name='map'),
]