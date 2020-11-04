from django.apps import AppConfig
from terra_settings.settings import TERRA_APPLIANCE_SETTINGS
from rest_framework_jwt.settings import api_settings

from .permissions_mixins import PermissionRegistrationMixin


class AccountsConfig(PermissionRegistrationMixin, AppConfig):
    name = 'terra_accounts'
    verbose_name = 'Terra Accounts'

    permissions = (
        ('can_manage_users', 'User: Is able to create, delete, update users'),
        ('can_manage_groups', 'User: Is able to create, delete, update groups'),
    )

    def ready(self):
        # terra_accounts need to add jwt_delta key in terra-settings settings endpoint
        TERRA_APPLIANCE_SETTINGS.setdefault('jwt_delta', api_settings.JWT_EXPIRATION_DELTA)
        super().ready()
