from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Permission, User
#from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CustomUser(models.Model):

    #user has username, password, email, firstname, lastname 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    '''
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    '''
    mobileNumber = models.IntegerField(null=True)
    dateOfBirth = models.DateField(null=True)
    gender = models.CharField(null=True, max_length=10)
    uniqueCode = models.IntegerField(null=True)
    #mobileNumber
    #dateOfBirth
    #gender
    #uniqueCode
    

    def __str__(self):
        return self.user.username