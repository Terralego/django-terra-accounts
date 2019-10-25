from django.apps import AppConfig
from django.conf import settings
from rest_framework_jwt.settings import api_settings

from .permissions_mixins import PermissionRegistrationMixin


class AccountsConfig(PermissionRegistrationMixin, AppConfig):
    name = 'terra_accounts'
    verbose_name = 'Terra Accounts'

    permissions = (
        ('can_manage_users', 'Is able to create, delete, update users'),
        ('can_manage_groups', 'Is able to create, delete, update groups'),
    )

    def ready(self):
        # terra_accounts need to add jwt_delta key in terra_utils settings endpoint
        terra_settings = getattr(settings, 'TERRA_APPLIANCE_SETTINGS', {})
        terra_settings.setdefault('jwt_delta', api_settings.JWT_EXPIRATION_DELTA)
        super().ready()
