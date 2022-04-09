from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Permission, User
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# Create your models here.
class CustomUser(models.Model):
    gender_choices = ( ('M', 'Male'), ('F', 'Female'), )

    #user has username, password, email, firstname, lastname 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    '''
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    '''
    phoneNumber = PhoneNumberField(unique = True, null = True, blank = True)
    dateOfBirth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=gender_choices, null=True)
    uniqueCode = models.UUIDField(unique=True, default=uuid.uuid4().hex, blank=True)
    wallet = models.FloatField(default=float(100000))
    

    def __str__(self):
        return self.user.username