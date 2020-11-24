from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from terra_accounts.models import TerraPermission
from url_filter.integrations.drf import DjangoFilterBackend

from . import serializers
from .filters import JSONFieldOrderingFilter
from .forms import PasswordSetAndResetForm
from .permissions import GroupAdminPermission, UserAdminPermission

UserModel = get_user_model()


class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        form = PasswordSetAndResetForm(data=request.data)
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
        try:
            if form.is_valid():
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

                serializer = serializers.TerraUserSerializer(user)

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
    permission_classes = (permissions.AllowAny, )

    def post(self, request, uidb64, token):
        serializer = serializers.PasswordResetSerializer(uidb64, token, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user_serializer = serializers.TerraUserSerializer()
        return Response(user_serializer.to_representation(serializer.user))


class UserChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = serializers.PasswordChangeSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user_serializer = serializers.TerraUserSerializer()
        return Response(user_serializer.to_representation(serializer.user))


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    filter_backends = (DjangoFilterBackend, JSONFieldOrderingFilter,
                       SearchFilter, )
    search_fields = ('uuid', 'email', 'properties', )
    filter_fields = ('uuid', 'email', 'properties', 'groups', 'is_superuser',
                     'is_active', 'is_staff', 'date_joined')

    def get_serializer_class(self):
        """ in write endpoints, use customs serializers to avoid privilege escalation """
        if self.request.method not in permissions.SAFE_METHODS:
            user = self.request.user
            if not user.is_superuser:
                return serializers.TerraStaffUserSerializer if user.is_staff else serializers.TerraSimpleUserSerializer
        return serializers.TerraUserSerializer

    def get_permissions(self):
        """ Simple Auth to access profile, Admin perm to manage viewset """
        if self.action == "profile":
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticated, UserAdminPermission]
        return super().get_permissions()

    @action(detail=False, serializer_class=serializers.TerraUserSerializer, methods=["get"])
    def profile(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, GroupAdminPermission, )
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class TerraPermissionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = TerraPermission.objects.all()
    serializer_class = serializers.TerraPermissionSerializer

    @action(detail=False, serializer_class=serializers.TerraPermissionSerializer, methods=["get"])
    def available(self, request, *args, **kwargs):
        """ List only logged user permission """
        perms = request.user.terra_permissions
        serializer = self.get_serializer(perms, many=True)
        return Response(serializer.data)
