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
    """
    param: request
    functionality: The user login's to the page via this function
    return: to a page based on user actions
    """
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
            return redirect('/accounts/login')
    else:
        return render(request, 'login.html')



def register(request):
    """
    param: request
    functionality: The user register's via this function
    return: to a page based on user actions
    """
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
    """
    param: request
    functionality: Token based authentication is checked via this function and the user is provided with
    some extra views if the token is authenticated
    return: to a page based on user actions
    """
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
    """
    param: request
    functionality: Logout action is carried out via this function
    return: to a page based on user actions
    """

    #print(request.user)
    if not request.user.is_authenticated:
        messages.error(request, "Your session was expired please Login again",)
        ExpiringToken.objects.all().delete()
        auth.logout(request)
        #return redirect('product_view', kwargs={'product_id': featured_products[0].id})
        #kwargs = {'product_id': featured_products[0].id}
        #return render(request,'', {'alert_flag': True})
        #return render(request,'/index', {'alert_flag': True})
        return redirect('/',kwargs={'alert_flag': True})
    else:
        token = ExpiringToken.objects.get(user= request.user)
        print(token)
        token.delete()
        auth.logout(request)
        return redirect('/')
