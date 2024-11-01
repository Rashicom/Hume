from django.urls import path
from . import views

urlpatterns = [
    path('add-readings/', views.AddReadings.as_view(), name="add-readings"),
    path('test/', views.Test.as_view(),)
    
]