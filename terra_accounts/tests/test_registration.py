import json

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

from .factories import TerraUserFactory


class RegistrationTestCase(TestCase):

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_registration_view(self):
        # Testing with good email
        response = self.client.post(
            reverse('register'),
            {
                'email': 'toto@terra.com',
            })

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual('application/json', response['Content-Type'])
        self.assertIn(b'id', response.content)
        self.assertIn(b'email', response.content)
        self.assertIn(b'uuid', response.content)
        self.assertIn(b'group', response.content)

        # Testing duplicate email
        response = self.client.post(
            reverse('register'),
            {
                'email': 'toto@terra.com',
            }
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_reset_password(self):
        user = TerraUserFactory()

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Not same password
        response = self.client.post(
            reverse('reset-password', args=[uidb64, token]),
            {
                'new_password1': 'pass1',
                'new_password2': 'pass1false',
            }
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # Good password and set profile
        new_password = "thisismynewpassword"
        test_user_properties = {'test': 'property'}
        self.assertFalse(user.check_password(new_password))
        response = self.client.post(
            reverse('reset-password', args=[uidb64, token]),
            {
                'new_password1': new_password,
                'new_password2': new_password,
                'properties': json.dumps(test_user_properties)
            }
        )

        user.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(user.check_password(new_password))
        self.assertDictEqual(user.properties, test_user_properties)

    def test_invalid_email(self):
        response = self.client.post(
            reverse('register'),
            {
                'email': 'toto@terra.',
            })
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        # Testing email is empty
        response = self.client.post(
            reverse('register'),
            {
                'email': '',
            }
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_already_existing_email_registration(self):
        test_email = 'test@test.com'
        TerraUserFactory(email=test_email)

        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(
            reverse('register'),
            {
                'email': test_email,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual({}, response.json())
        self.assertEqual(
            get_user_model().objects.filter(email=test_email).count(),
            1
        )
        self.assertEqual(len(mail.outbox), 1)
