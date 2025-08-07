from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from common.models import BaseModel
from .managers import AccountManager
# Create your models here.


class Account(BaseModel,AbstractBaseUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        ADMIN = "ADMIN"
        DATA_COLLECTOR = "DATA_COLLECTOR"
        STUDENTS = "STUDENTS"
        RESEARCHER = "RESEARCHER"
        INSTITUTES = "INSTITUTES"
    
    mobile_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=UserRole, default=UserRole.DATA_COLLECTOR)

    # Django Level Permissions Use only for Django Admin
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)
    
    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []

    objects = AccountManager()
    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
            # Only hash the password if it's not already hashed
            self.set_password(self.password)
        super().save(*args, **kwargs)



