from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from terra_accounts.tests.factories import TerraUserFactory

UserModel = get_user_model()


class AuthenticationTestCase(APITestCase):
    USER_PASSWORD = '123456'

    def setUp(self):
        self.user = TerraUserFactory.create(password=self.USER_PASSWORD)

    def test_authentication_jwt(self):
        """Feature with valid properties is successfully POSTed"""
        response = self.client.post(reverse('token-obtain'),
                                    {'email': self.user.email,
                                     'password': self.USER_PASSWORD},)

        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)

        token = response.data.get('token', False)

        response = self.client.post(reverse('token-verify'),
                                    {'token': token, },)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(token, response.data.get('token'))

    def test_fail_authentication(self):
        response = self.client.post(reverse('token-obtain'),
                                    {'email': 'invalid@user.com',
                                     'password': self.USER_PASSWORD},)

        self.assertEqual(response.status_code, 400)
        self.assertIn('non_field_errors', response.data)

    def test_create_superuser(self):
        superuser = UserModel.objects.create_superuser('admin@bar.com',
                                                       '123456')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
