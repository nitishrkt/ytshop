from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework import exceptions
# Write your serializer here...
'''
User serializer where email is optional

'''
class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    class Meta:
        model = User
        fields = ('phone', 'name', 'password', 'email',)
    
    def create(self, validated_data):
        user = super(UserRegistrationSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

'''
Login serializer with login auth using phone number
'''

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")
        if phone and password:
            user = authenticate(username=phone, password=password)
            # if user.is_active:
            data["user"]=user
            # else:
            #     msg = "User is deactivated"
            #     raise exceptions.ValidationError(msg)
        else:  
            msg = "Must provide Username and Password"
            raise exceptions.ValidationError(msg)
        return data

