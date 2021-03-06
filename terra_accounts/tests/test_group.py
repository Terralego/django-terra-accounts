from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import TerraUserFactory

UserModel = get_user_model()


class UserViewsetTestCase(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(name='test group')
        self.user = TerraUserFactory()
        self.user.groups.add(self.group)

        self.client.force_authenticate(user=self.user)
        self.user.user_permissions.add(
            *Permission.objects.filter(codename__in=['can_manage_groups', ])
        )

    def test_group_detail(self):
        response = self.client.get(
            reverse('group-detail', args=[self.group.pk])
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # The user must be in the group
        self.assertIn(self.user.id, response.data['users'])
        # and we must have the group name in the response
        self.assertEqual(self.group.name, response.data['name'])

    def test_create_group(self):
        data = {
            "name": "test group 3"
        }
        response = self.client.post(
            reverse('group-list'),
            data,
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # We must have only 2 groups in the DB
        self.assertEqual(2, Group.objects.count())
        # And their must be no users in this new group
        self.assertEqual(0, Group.objects.get(name=data["name"]).user_set.count())

    def test_create_group_with_user(self):
        data = {
            "name": "test group 2",
            "users": [self.user.id],
        }
        response = self.client.post(
            reverse('group-list'),
            data,
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn(self.user.id, response.data['users'])
        # And also test than the user is in the DB
        self.assertIn(self.user.id, Group.objects.get(name=data["name"]).user_set.values_list('id', flat=True))

    def test_only_terrauser_can_create_group(self):
        self.user.user_permissions.clear()
        data = {
            "name": "test group 2",
            "users": [self.user.id],
        }
        response = self.client.post(
            reverse('group-list'),
            data,
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_partial_update_name_group(self):
        data = {
            "name": "new group name"
        }
        response = self.client.patch(
            reverse('group-detail', args=[self.group.pk]),
            data,
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # We must still have only 1 group in the DB
        self.assertEqual(1, Group.objects.count())
        # but with the new name
        self.assertEqual(data["name"], Group.objects.get(pk=self.group.pk).name)
        # And still have one user in it
        self.assertEqual(1, Group.objects.get(pk=self.group.pk).user_set.count())

    def test_partial_update_user_group(self):
        new_user = TerraUserFactory()
        data = {
            "users": [new_user.id],
        }
        response = self.client.patch(
            reverse('group-detail', args=[self.group.pk]),
            data,
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # We must still have only 1 group in the DB
        self.assertEqual(1, Group.objects.count())
        # but with the new user inside
        self.assertIn(new_user.email, Group.objects.get(name=self.group.name).user_set.values_list('email', flat=True))
        # and only one user in this group
        self.assertEqual(1, Group.objects.get(name=self.group.name).user_set.count())
        # and still have the same name
        self.assertEqual(self.group.name, Group.objects.get(pk=self.group.pk).name)

    def test_update_group_with_new_user(self):
        new_user = TerraUserFactory()
        data = {
            "name": "new group name",
            "users": [new_user.id],
        }
        response = self.client.put(
            reverse('group-detail', args=[self.group.pk]),
            data,
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.json())
        # We must still have only 1 group in the DB
        self.assertEqual(1, Group.objects.count())
        # but with the new name
        self.assertEqual(data["name"], Group.objects.get(name=data["name"]).name)
        # And still have one user in it
        self.assertEqual(1, Group.objects.get(name=data["name"]).user_set.count())
        # but the user should be the new one
        self.assertIn(new_user.email, Group.objects.get(name=data["name"]).user_set.values_list('email', flat=True))

    def test_delete_group(self):
        response = self.client.delete(
            reverse('group-detail', args=[self.group.pk])
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Group.objects.count())
