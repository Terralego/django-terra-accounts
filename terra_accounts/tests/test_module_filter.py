from unittest.mock import patch
from django.test import TestCase, modify_settings, override_settings

from terra_accounts.models import TerraPermission
from terra_accounts.serializers import TerraUserSerializer


class ManagerPermissionTestCase(TestCase):
    @patch.dict(
        'terra_settings.settings.TERRA_APPLIANCE_SETTINGS', 
        {'disabled_modules': []}
    )
    def test_all_permission_return(self):
        q = TerraPermission.objects.all()
        self.assertEqual(q.count(), 3, q.count())
    
    @patch.dict(
        'terra_settings.settings.TERRA_APPLIANCE_SETTINGS', 
        {'disabled_modules': ['BaseLayer']}
    )
    def test_manager_filter(self):
        from terra_settings.settings import TERRA_APPLIANCE_SETTINGS
        qf = TerraPermission.objects.all()
        self.assertEqual(qf.count(), 2, qf.count())


        


    
