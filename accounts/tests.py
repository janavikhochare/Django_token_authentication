from django.test import TestCase

from django.contrib.auth import (
    BACKEND_SESSION_KEY, HASH_SESSION_KEY, REDIRECT_FIELD_NAME, SESSION_KEY,
)


from datetime import timedelta
from time import sleep

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django_expiring_token.models import ExpiringToken
# Create your tests here.

class AuthViewsTestCase(TestCase):
    """
    Test the authentication """

    def setUp(self):
        """Create a user and associated token."""
        self.username = 'test_username'
        self.email = 'test@g.com'
        self.password = 'test_password'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

        self.key = 'jhfbgkjasnlkfmlkn'
        self.token = ExpiringToken.objects.create(
            user=self.user,
            key=self.key
        )
        self.client = APIClient()
    # @classmethod
    # def setUpTestData(cls):
    #     cls.u1 = User.objects.create_user(first_name="test-first-name", last_name="test-last-name",username='testclient', password='password', email='testclient@example.com')
    #     cls.u3 = User.objects.create_user(first_name="test-staff-first-name", last_name="test-staff-last-name",username='staff', password='password', email='staffmember@example.com')

    def login(self, username='test_username', password='test_password'):
        response = self.client.post('/accounts/login/', {
            'username': username,
            'password': password,
        })
        self.assertIn(SESSION_KEY, self.client.session)
        return response

    def logout(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)

    # def assertFormError(self, response, error):
    #     """Assert that error is found in response.context['form'] errors"""
    #     form_errors = list(itertools.chain(*response.context['form'].errors.values()))
    #     self.assertIn(str(error), form_errors)


    def test_create_token(self):
        user = User.objects.create_user(
            username="test",
            email="",
            password="abcd1234"
        )
        data = {'username': 'test', 'password': 'abcd1234'}
        resp = self.client.post(reverse('accounts/token_authenti'), data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_obtain_token_no_credentials(self):
        resp = self.client.post(reverse('accounts/token_authenti'))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_replace_expired_token(self):
        self.token.delete()
        token = ExpiringToken.objects.create(user=self.user)
        key_1 = token.key

        data = {'username': 'test_username', 'password': 'test_password'}

        with self.settings(EXPIRING_TOKEN_DURATION=timedelta(milliseconds=1)):
            sleep(0.005)
            resp = self.client.post(reverse('accounts/token_authenti'), data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        token = ExpiringToken.objects.first()
        key_2 = token.key
        self.assertEqual(token.user, self.user)
        self.assertEqual(resp.data['token'], token.key)
        self.assertTrue(key_1 != key_2)
