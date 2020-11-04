from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AppTestCase(APITestCase):
    def test_settings_default(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn('jwt_delta', data)
        self.assertEqual(data['jwt_delta'], "9999.0")
