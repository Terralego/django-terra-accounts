from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class SettingsViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(200, response.status_code)
        self.assertListEqual(
            ['jwt_delta', 'language', 'base_layers'],
            list(response.json())
        )
