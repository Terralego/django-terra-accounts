from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AppTestCase(APITestCase):
    @override_settings(JWT_AUTH={'JWT_EXPIRATION_DELTA': 9999})
    def test_settings_patched(self):
        response = self.client.get(reverse('terra_accounts:settings'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data['jwt_delta'], 9999)

    def test_settings_default(self):
        response = self.client.get(reverse('terra_accounts:settings'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertNotEqual(data['jwt_delta'], 9999)
