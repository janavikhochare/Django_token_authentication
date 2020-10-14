from django.db import models


# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import  Token
#
#
# # Create your models here.
#
# @receiver(post_save,sender =settings.AUT)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserUniqueToken(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    datetime = models.DateField(default=timezone.now)  # for token expiration