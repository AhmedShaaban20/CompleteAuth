import email
from genericpath import exists
from importlib.util import set_loader

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os

from .serializer import *
from .emails import *


class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'message' : 'registration successfully check email',
                    'data' : serializer.data,
                },status=status.HTTP_201_CREATED)

            return Response({
            'message' : 'something went wrong',
            'data' : serializer.errors,
             },status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
            'error' : str(e),
             },status= status.HTTP_400_BAD_REQUEST)

class VerifyEmailAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = ResetAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']  
                users = User.objects.filter(email = email)
                if not users:
                    return Response({
                    'status': 400,
                    'data' : 'invalid email'
                },status= status.HTTP_400_BAD_REQUEST)
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'message' : 'sent otp, check email',
                    'data' : serializer.data,
                },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
            'error' : str(e),
             },status= status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                users = User.objects.filter(email = email)
                if not users:
                    return Response({
                    'status': 400,
                    'data' : 'invalid email'
                },status= status.HTTP_400_BAD_REQUEST)

                if users[0].otp != otp:
                    return Response({
                    'status': 400,
                    'data' : 'wrong otp'
                },status= status.HTTP_400_BAD_REQUEST)
                if users[0].otp == otp:
                    users[0].is_verified = True
                    users[0].save()
                    return Response({
                        'message' : 'account verified, go to reset password',
                        'data' : {}
                    },status=status.HTTP_200_OK)
        
                
            return Response({
            'message' : 'something went wrong',
            'data' : serializer.errors,
            },status= status.HTTP_405_METHOD_NOT_ALLOWED) 

        except Exception as e:
            return Response({
            'error' : str(e),
             },status= status.HTTP_400_BAD_REQUEST)

        
class SetNewPasswordAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = SetNewPasswordSerializer(data=data)

            users = User.objects.get(email = email)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                password = serializer.data['password']
                if not users:
                    return Response({
                    'status': 400,
                    'data' : 'invalid email'
                },status= status.HTTP_400_BAD_REQUEST)

                if users[0].otp != otp:
                    return Response({
                    'status': 400,
                    'data' : 'wrong otp'
                },status= status.HTTP_400_BAD_REQUEST)
                if users[0].otp == otp:
                    users[0].is_verified = True
                    users[0].set_password(password)
                    users[0].save()
                    return Response({
                        'message' : 'changed password successfully',
                        'data' : {}
                    },status=status.HTTP_200_OK)
        
                
            return Response({
            'message' : 'something went wrong',
            'data' : serializer.errors,
            },status= status.HTTP_405_METHOD_NOT_ALLOWED) 

        except Exception as e:
            return Response({
            'error' : str(e),
             },status= status.HTTP_400_BAD_REQUEST)

    

        