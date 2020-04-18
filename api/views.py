from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import login as django_login, logout as django_logout

# Create your views here.
'''
User registration view 
url = /api/register/
'''
class UserRegistration(APIView):

    authentication_classes=[]
    permission_classes=[]
    parser_classes = [JSONParser]
    def post(self, request):
        print(request.data)
        serializer = UserRegistrationSerializer(data= request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'True'})
        return Response({'status':'False'})

'''
Login view using phone number 
url =  /api/login/
'''

class LoginView(APIView): 
    authentication_classes=[]
    permission_classes=[]      

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token":token.key}, status=200)

'''
logout view and deleting the session
url = /api/logout
'''
class LogoutView(APIView):

    def get(self, request):
        # authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
        django_logout(request)
        return Response(status=204)