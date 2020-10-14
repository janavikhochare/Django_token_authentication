from django.urls import path
from . import views
#from .views import ObtainExpiringAuthToken
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url


#from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("token_authenti", views.token_authenti, name="token_authenti"),
    #path("aftertoken", views.destt, name="aftertoken"),
    path("logout", views.logout, name="logout"),
    path('custom-url/', include('django_expiring_token.urls')),
    #path('login/<str:token>', user_form, name='user-form')
    #path(r'^token/', views.obtain_expiring_auth_token)
]

# urlpatterns += [
#     path('token/',ObtainExpiringAuthToken.as_view()),
# ]


