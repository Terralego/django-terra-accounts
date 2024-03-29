from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from terra_accounts.tests.factories import TerraUserFactory


class SettingsViewTestCase(APITestCase):
    def test_settings_patched(self):
        """ public settings provided by terra_settings endpoint should serve jwt_delta value patched in apps.ready """
        response = self.client.get(reverse('settings'))
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIn('jwt_delta', data)


class UserViewsetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = TerraUserFactory(is_staff=True, is_superuser=True)

    def setUp(self) -> None:
        self.client.force_authenticate(self.superuser)

    def test_detail(self):
        response = self.client.get(reverse('user-detail', args=(self.superuser.pk, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # module User should appear in modules list
        self.assertListEqual(sorted(data['modules']), sorted(['BaseLayer', 'User', 'UserGroup']))


class TerraPermissionViewsetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = TerraUserFactory(is_staff=True, is_superuser=True)
        cls.simple_user = TerraUserFactory()

    def setUp(self) -> None:
        self.client.force_authenticate(self.superuser)

    def test_list_superuser(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.get(reverse('permission-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # module User should appear in modules list
        self.assertTrue(len(data) > 1)

    def test_available_superuser(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.get(reverse('permission-available'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # module User should appear in modules list
        self.assertTrue(len(data) > 1)

    def test_list_simpleuser(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('permission-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # module User should appear in modules list
        self.assertTrue(len(data) > 1)

    def test_available_simpleuser(self):
        self.client.force_authenticate(self.simple_user)
        response = self.client.get(reverse('permission-available'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # module User should appear in modules list
        self.assertTrue(len(data) == 0)
