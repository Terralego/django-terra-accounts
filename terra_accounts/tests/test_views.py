from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class SettingsViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_settings_patched(self):
        """ public settings provided by terra_settings endpoint should serve jwt_delta value patched in apps.ready """
        response = self.client.get(reverse('settings'))
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIn('jwt_delta', data)
