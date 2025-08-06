from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('edit-account/', views.EditAccount.as_view(), name='edit-account'),
    
    path('news/', views.News.as_view(), name='news'),
    path('about/', views.About.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('rain-pattern/', views.RainPattern.as_view(), name='rain-pattern'),
    path('temp-pattern/', views.TemperaturePattern.as_view(), name='temp-pattern'),
    path('gallery/', views.Gallery.as_view(), name='gallery'),

    path('map/', views.TestMap.as_view(), name='map'),

    # admin login
    path('admin/login/', views.AdminLogin.as_view(), name="admin_login"),
    path('admin/logout/', views.AdminLogout.as_view(), name="admin_logout")

]