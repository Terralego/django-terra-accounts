import logging
from django.conf import settings


logger = logging.getLogger(__name__)


def permission_callback(sender, **kwargs):
    logger.info(f"Updating permissions of {sender.name}")

    ContentType = sender.apps.get_model("contenttypes.ContentType")
    TerraPermission = sender.apps.get_model("terra_accounts.TerraPermission")

    for module, perm, name in sender.permissions:
        if module in settings.TERRA_APPLIANCE_SETTINGS["disabled_modules"]:
            continue

        ctype = ContentType.objects.get_for_model(TerraPermission)

        TerraPermission.objects.update_or_create(
            content_type=ctype,
            codename=perm,
            defaults={
                "name": name,
                "module": module
            }
        )
