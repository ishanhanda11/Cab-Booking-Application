from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.
class UserManger(BaseUserManager):
    def create_user(self, email, password=None, role='PASSENGER'):
        if not email:
            raise ValueError("Users must have an email!")