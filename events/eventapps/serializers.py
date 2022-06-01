from rest_framework import serializers
from .models import *


# class ProfileSerializer(Serializers.ModelSerializer):
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','password')

class ProfileSerialzer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'

   