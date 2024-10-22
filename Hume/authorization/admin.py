from django.contrib import admin
from .models import Account
# Register your models here.


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'email', 'name', 'role', 'is_staff', 'is_active')