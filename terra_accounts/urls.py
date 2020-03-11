from django.conf.urls import url
from django.contrib.auth import views as base_auth_views
from django.urls import path
from rest_framework import routers
from rest_framework.reverse import reverse_lazy
from rest_framework_jwt import views as auth_views

from .views import (DeprecatedUserViewSet, GroupViewSet,
                    UserChangePasswordView, UserInformationsView,
                    UserProfileView, UserRegisterView, UserSetPasswordView,
                    UserViewSet)

app_name = 'terra_accounts'

router = routers.SimpleRouter()
router.register(r'user', DeprecatedUserViewSet, basename='user')
router.register(r'user', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')
urlpatterns = router.urls

urlpatterns += [
    # jwt process
    path('auth/obtain-token/', auth_views.obtain_jwt_token, name='token-obtain'),
    path('auth/verify-token/', auth_views.verify_jwt_token, name='token-verify'),
    path('auth/refresh-token/', auth_views.refresh_jwt_token, name='token-refresh'),

    # reset lost password
    path('auth/password-reset/', base_auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('terra_accounts:password_reset_done'),
        email_template_name='registration/accounts_password_reset_email.html'), name='password_reset'),
    path('auth/password-reset/done/', base_auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^auth/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        base_auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('terra_accounts:password_reset_complete'),), name='password_reset_confirm'),
    path('auth/reset/done/', base_auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # account management
    path('auth/user/', UserInformationsView.as_view()),
    path('accounts/user/', UserProfileView.as_view(), name='profile'),
    path('accounts/register/', UserRegisterView.as_view(), name='register'),
    url((r'^accounts/change-password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
         r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'),
        UserSetPasswordView.as_view(), name='reset-password'),
    path('accounts/change-password/reset/', UserChangePasswordView.as_view(), name='new-password'),
]
