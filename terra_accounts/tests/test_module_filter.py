from django.test import TestCase, override_settings

from terra_accounts.models import TerraPermission


class ManagerPermissionTestCase(TestCase):
    @override_settings(TERRA_APPLIANCE_SETTINGS={'disabled_modules': []})
    def test_all_permission_return(self):
        q = TerraPermission.objects.all()
        self.assertEqual(q.count(), 3, q.count())

    @override_settings(TERRA_APPLIANCE_SETTINGS={'disabled_modules': ['BaseLayer']})
    def test_manager_filter(self):
        qf = TerraPermission.objects.all()
        self.assertEqual(qf.count(), 2, qf.count())
