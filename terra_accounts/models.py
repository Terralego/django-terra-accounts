import importlib

import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, _user_has_perm
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import ReadModelManager, TerraUserManager


class TerraUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    uuid = models.CharField(_('unique identifier'),
                            max_length=255,
                            default=uuid.uuid4,
                            unique=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    properties = JSONField(default=dict, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user '
                    'can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = TerraUserManager()

    def get_by_natural_key(self, username):
        return self.get(**{f'{self.model.USERNAME_FIELD}__iexact': username})

    def get_all_terra_permissions(self):
        if self.is_active:
            if self.is_superuser:
                perms = TerraPermission.objects.all()
            else:
                perms = self.user_permissions.filter(terrapermission__isnull=False)
        else:
            perms = TerraPermission.objects.none()

        return perms.values_list('codename', flat=True)

    def has_terra_perm(self, codename):
        return _user_has_perm(self, f'{self._meta.app_label}.{codename}', None)

    def __str__(self):
        try:
            path = settings.TERRA_USER_STRING_FORMAT
            module_path, attr_name = path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, attr_name)(self)
        except AttributeError:
            return self.email

    class Meta:
        ordering = ['id']


UserModel = get_user_model()


class TerraPermission(Permission):
    original = models.OneToOneField(Permission, on_delete=models.CASCADE, parent_link=True)


class ReadModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    contenttype = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    identifier = models.PositiveIntegerField()
    model_object = GenericForeignKey('contenttype', 'identifier')
    last_read = models.DateTimeField(auto_now=True)

    objects = ReadModelManager()

    def read_instance(self):
        self.save()

    class Meta:
        ordering = ['id']
