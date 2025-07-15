from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, ThingsReadingsView, ClusterView, WeatherHistoryView

urlpatterns = [
    path("login", LoginView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),

    path("things", ThingsReadingsView.as_view()),
    path("cluster", ClusterView.as_view()),
    path("weather-history/<uuid:pk>", WeatherHistoryView.as_view()),
    
]