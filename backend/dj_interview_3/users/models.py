from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = PhoneNumberField(unique=False, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    about_me = models.TextField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='new_photos/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'
