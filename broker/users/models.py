from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class CustomUser(AbstractBaseUser):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username