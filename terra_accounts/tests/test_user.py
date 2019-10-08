from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import IntegrityError
from django.urls import reverse
from rest_framework.test import APITestCase

from .factories import TerraUserFactory

UserModel = get_user_model()


class UserViewsetTestCase(APITestCase):
    def setUp(self):
        self.user = TerraUserFactory()
        self.client.force_authenticate(user=self.user)

    def test_no_permission(self):
        response = self.client.get(reverse('terra_accounts:user-list')).json()
        # List must be empty with no rights
        self.assertEqual(0, response.get('count'))

    def test_userlist(self):
        self.user.user_permissions.add(
            *Permission.objects.filter(codename__in=['can_manage_users', ])
        )
        response = self.client.get(reverse('terra_accounts:user-list')).json()
        # List must contain all database users
        self.assertEqual(UserModel.objects.count(), response.get('count'))

    def test_update_uuid(self):
        user = TerraUserFactory()
        self.user.user_permissions.add(
            *Permission.objects.filter(codename__in=['can_manage_users'])
        )

        test_uuid = 'test-uuid'
        response = self.client.patch(
            f'/api/user/{user.uuid}/',
            {
                'uuid': test_uuid,
            }
        )
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.uuid, test_uuid)

    def test_update_uuid_deprecated(self):
        user = TerraUserFactory()
        self.user.user_permissions.add(
            *Permission.objects.filter(codename__in=['can_manage_users'])
        )

        test_uuid = 'test-uuid'
        response = self.client.patch(
            f'/api/user/{user.id}/',
            {
                'uuid': test_uuid,
            }
        )
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.uuid, test_uuid)

    def test_create_two_user_with_same_email(self):
        with self.assertRaises(IntegrityError):
            UserModel.objects.create(email=self.user.email)
