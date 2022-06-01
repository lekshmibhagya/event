from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=254)
    phonenumber=PhoneNumberField()
    def __str__(self):
        return "{}-{}".format(self.name,self.email)
    

class Event(models.Model):
    event_name=models.CharField(max_length=30)
    about=models.CharField(max_length=200)
    location=models.CharField(max_length=100)
    start_date=models.DateField()
    end_date=models.DateField()
    image=models.ImageField(upload_to='image/',max_length=100)
    owner=models.ForeignKey(Profile,related_name='owner',on_delete=models.CASCADE,)
    def __str__(self):
        return "{}".format(self.event_name)