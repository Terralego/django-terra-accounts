from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import TerraUserFactory


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.user = TerraUserFactory()

    def test_user_profile(self):
        """ Tests all operations on user profile """

        # unauthenticated user must be stopped
        response = self.client.get(reverse('profile'))
        self.assertEqual(401, response.status_code)

        # let's try with an authenticated user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('profile'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(str(self.user.uuid), response.json()['uuid'])
