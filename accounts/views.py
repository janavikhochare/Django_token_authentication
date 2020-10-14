from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.urls import reverse
#from rest_framework.authtoken.models import Token
from django_expiring_token.views import LoginView
import requests
from django_expiring_token.models import ExpiringToken
from django.conf import settings
from django_expiring_token.authentication import ExpiringTokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import timedelta
import datetime
from django.utils.timezone import utc
import pytz

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            #token = Token.objects.get(user=user).key
            token= ExpiringToken.objects.create(user=user).key
            created_token = ExpiringToken.objects.get(user=request.user).created
            expired_token = ExpiringToken.objects.get(user=request.user).expires

            # print(created_token)
            print(expired_token)
            print(expired_token-created_token)
            # print(user)
            print(token)

            return redirect("/accounts/token_authenti")
            #return render(request,redirect('/'),{'token':token})
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')



def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User name taken')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email id taken")
                return redirect('register')

            else:
                user = User.objects.create_user(username=username, email=email, password=password1,
                                                first_name=first_name, last_name=last_name)
                #token = Token.objects.create(user=user)

                user.save();
                messages.info(request, 'User Created')
                #print("Token generated " , token)
                print('User Created')
                return redirect('/accounts/login')

        else:
            messages.info(request, "Password not matching")
            return redirect('/')

        return redirect('/')
    else:
        return render(request, 'register.html')

def token_authenti(request):
    if request.method == 'POST':
        username = request.POST['username']
        user_token= request.POST['token']

        token = ExpiringToken.objects.get(user=request.user).key
        created_token = ExpiringToken.objects.get(user=request.user).created
        expired_token = ExpiringToken.objects.get(user=request.user).expires
        #print()
        #user_token = get_object_or_404(user_token, token=token)  # get object or throw 404

        print(created_token)
        print(expired_token)
        print(expired_token-created_token)
        print(user_token)

        if user_token == token:
            return redirect('/')
        else:
            messages.info(request, "Token not matching")

        # if(expired_token-created_token) < timedelta(seconds=300):# check if stored time exceeds 2 hours
        #     messages.info(request,"Login again your token is expired")
        #     return render(request,'login.html')
        # else:
        #     return redirect('/')
    return render(request,'token_authenti.html')

def logout(request):
    print(request.user)
    if not request.user.is_authenticated:
        messages.error(request, "Your session was expired please Login again",)
        ExpiringToken.objects.all().delete()
        auth.logout(request)
        #return render(request,'', {'alert_flag': True})
        #return render(request,'/index', {'alert_flag': True})
        return redirect('/',{'alert_flag': True})
    else:
        token = ExpiringToken.objects.get(user= request.user)
        print(token)
        token.delete()
        auth.logout(request)
        return redirect('/')



# from .models import UserUniqueToken
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from datetime import timedelta
#
# @login_required
# def user_form(request, token):
#     user_token = get_object_or_404(UserUniqueToken, token=token)  # get object or throw 404
#     time_now = timezone.now()  # get current time
#     if user_token.datetime > (time_now - timedelta(hours=0.01)):# check if stored time exceeds 2 hours
#         messages.info(request,"Login again")
#     return render(request,'login.html')


# import datetime
# from django.utils.timezone import utc
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from django.http import HttpResponse
# import json
# from rest_framework import status

# class ObtainExpiringAuthToken(ObtainAuthToken):
#     def post(self, request):
#         serializer = self.serializer_class(data=request.DATA)
#         if serializer.is_valid():
#             token, created =  Token.objects.get_or_create(user=serializer.object['user'])
#
#             utc_now = datetime.datetime.utcnow()
#             if not created and token.created < utc_now - datetime.timedelta(hours=1):
#                 token.delete()
#                 token = Token.objects.create(user=serializer.object['user'])
#                 token.created = datetime.datetime.utcnow()
#                 token.save()
#
#             #return Response({'token': token.key})
#             response_data = {'token': token.key}
#             return HttpResponse(json.dumps(response_data), content_type="application/json")
#
#         return HttpResponse(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
#
# obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

# import datetime
# from pytz import utc
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.serializers import AuthTokenSerializer
#
#
# class ObtainExpiringAuthToken(ObtainAuthToken):
#     def post(self, request, **kwargs):
#         serializer = AuthTokenSerializer(data=request.data)
#
#         if serializer.is_valid():
#             token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
#             if not created:
#                 # update the created time of the token to keep it valid
#                 token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
#                 token.save()
#
#             return Response({'token': token.key})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)