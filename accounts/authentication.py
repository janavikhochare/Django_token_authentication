# import datetime
# from django.utils.timezone import utc
# from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
#
# class ExpiringTokenAuthentication(TokenAuthentication):
#     def authenticate_credentials(self, key):
#
#         try:
#             token = self.model.objects.get(key=key)
#         except self.model.DoesNotExist:
#             raise exceptions.AuthenticationFailed('Invalid token')
#
#         if not token.user.is_active:
#             raise exceptions.AuthenticationFailed('User inactive or deleted')
#
#         utc_now = datetime.datetime.utcnow()
#
#         if token.created < utc_now - datetime.timedelta(hours=1):
#             raise exceptions.AuthenticationFailed('Token has expired')
#
#         return (token.user, token)


from rest_framework.authentication import TokenAuthentication
from datetime import timedelta
from datetime import datetime
import datetime as dtime
import pytz

class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.now(dtime.timezone.utc)
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(hours=1):
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token
