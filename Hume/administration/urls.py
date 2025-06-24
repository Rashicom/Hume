from django.urls import path
from . import views

urlpatterns = [
    path("maps", views.AdminMapListingView.as_view(), name="admin-maps"),
    path("create-state", views.CreateState.as_view(), name="create-state"),
    path("delete-state/<str:uuid>", views.DeleteState.as_view(), name="delete-state"),
    path("delete-district/<str:uuid>", views.DeleteDistrict.as_view(), name="delete-district"),

    path("create-district", views.CreateDistrict.as_view(), name="create-district"),

    path("dashboard", views.AdminDash.as_view(), name="admin-dashboard"),
    path("accounts", views.AccountsManagement.as_view(), name="admin-accounts"),
    path("things", views.ThingsManagement.as_view(), name="admin-things"),
    path("data", views.DataManagement.as_view(), name="admin-data"),
    path("readings", views.ReadingsManagement.as_view(), name="admin-readings"),
    
]