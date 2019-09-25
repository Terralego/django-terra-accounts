from django.apps import AppConfig
from django.conf import settings
from rest_framework_jwt.settings import api_settings


class AccountsConfig(AppConfig):
    name = 'terra_accounts'
    verbose_name = 'Terra Accounts'

    def ready(self):
        # terra_accounts need to add jwt_delta key in terra_utils settings endpoint
        terra_settings = getattr(settings, 'TERRA_APPLIANCE_SETTINGS', {})
        terra_settings.setdefault('jwt_delta', api_settings.JWT_EXPIRATION_DELTA)
