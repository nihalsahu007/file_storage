from rest_framework import serializers
from .models import *

class StorageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = '__all__'

class CustomerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username','email','password']
