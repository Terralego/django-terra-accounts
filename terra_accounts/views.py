from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.settings import api_settings as jwt_settings
from terra_utils.filters import JSONFieldOrderingFilter
from terra_utils.settings import TERRA_APPLIANCE_SETTINGS
from url_filter.integrations.drf import DjangoFilterBackend

from .forms import PasswordSetAndResetForm
from .permissions import GroupAdminPermission
from .serializers import (DeprecatedTerraUserSerializer, GroupSerializer,
                          PasswordChangeSerializer, PasswordResetSerializer,
                          TerraUserSerializer, UserProfileSerializer)

UserModel = get_user_model()


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()


class UserRegisterView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        form = PasswordSetAndResetForm(data=request.data)
        try:
            if form.is_valid():
                opts = {
                    'token_generator': default_token_generator,
                    'from_email': settings.DEFAULT_FROM_EMAIL,
                    'email_template_name':
                        'registration/registration_email.txt',
                    'subject_template_name':
                        'registration/registration_email_subject.txt',
                    'request': self.request,
                    'html_email_template_name':
                        'registration/registration_email.html',
                }

                with transaction.atomic():
                    user = get_user_model().objects.create(
                        **{
                            get_user_model().EMAIL_FIELD: (
                                request.data['email']
                            ),
                            'is_active': self._user_default_status,
                        })
                    user.set_unusable_password()
                    user.save()

                form.save(**opts)

                serializer = TerraUserSerializer(user)

                if 'terracommon.events' in settings.INSTALLED_APPS:
                    from terracommon.events.signals import event
                    event.send(
                        self.__class__,
                        action="USER_CREATED",
                        user=user,
                        instance=user
                    )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=form.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            # If user already exists, email to reset the password instead
            form.save(**opts)
            return Response({}, status=status.HTTP_200_OK)

    @property
    def _user_default_status(self):
        try:
            return settings.TERRA_USER_CREATION_STATUS
        except AttributeError:
            return False


class UserSetPasswordView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, uidb64, token):
        serializer = PasswordResetSerializer(uidb64, token, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user_serializer = UserProfileSerializer()
        return Response(user_serializer.to_representation(serializer.user))


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = PasswordChangeSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user_serializer = UserProfileSerializer()
        return Response(user_serializer.to_representation(serializer.user))


class UserInformationsView(APIView):
    def get(self, request):
        user = self.request.user
        return Response(DeprecatedTerraUserSerializer(user).data)


class UserViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    parser_classes = (JSONParser, )
    serializer_class = TerraUserSerializer
    queryset = UserModel.objects.none()
    filter_backends = (DjangoFilterBackend, JSONFieldOrderingFilter,
                       SearchFilter, )
    search_fields = ('uuid', 'email', 'properties', )
    filter_fields = ('uuid', 'email', 'properties', 'groups', 'is_superuser',
                     'is_active', 'is_staff', 'date_joined')
    lookup_field = 'uuid'
    lookup_value_regex = '[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}'

    def get_queryset(self):
        if self.request.user.has_perm('terra_accounts.can_manage_users'):
            return UserModel.objects.all()

        return self.queryset


class DeprecatedUserViewSet(UserViewSet):
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'
    serializer_class = DeprecatedTerraUserSerializer

    def dispatch(self, *args, **kwargs):
        import warnings
        warnings.warn(
            "Looking up a user by `id` is deprecated, use `uuid` instead.",
            DeprecationWarning
        )
        return super().dispatch(*args, **kwargs)


class GroupViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, GroupAdminPermission, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SettingsView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        terra_settings = {
            'jwt_delta': jwt_settings.JWT_EXPIRATION_DELTA,
            # for the moment, language is fixed and defined by backend instance
            'language': settings.LANGUAGE_CODE
        }

        terra_settings.update(TERRA_APPLIANCE_SETTINGS)

        return Response(terra_settings)
