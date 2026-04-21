from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, role='PASSENGER', phone=None):
        if not email:
            raise ValueError("Users must have an email!")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role, phone=phone)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password):
        user = self.create_user(email,password, role='ADMIN')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('PASSENGER', 'Passenger'),
        ('DRIVER', 'Driver'),
        ('ADMIN', 'Admin'),
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email
    
class Course(models.Model):
    title       = models.CharField(max_length=200)
    instructor  = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    is_free     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    secret_code = models.CharField(max_length=50)

class Department(models.Model):
    name     = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

class Employee(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    salary     = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='employees')