from django.conf.urls import url
from django.contrib.auth import views as base_auth_views
from django.urls import path, include
from rest_framework import routers
from rest_framework.reverse import reverse_lazy
from rest_framework_jwt import views as auth_views

from .views import (GroupViewSet,
                    UserChangePasswordView,
                    UserRegisterView, UserSetPasswordView,
                    UserViewSet)

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    # jwt process
    path('auth/obtain-token/', auth_views.obtain_jwt_token, name='token-obtain'),
    path('auth/verify-token/', auth_views.verify_jwt_token, name='token-verify'),
    path('auth/refresh-token/', auth_views.refresh_jwt_token, name='token-refresh'),

    # reset lost password
    path('auth/password-reset/', base_auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('password_reset_done'),
        email_template_name='registration/accounts_password_reset_email.html'), name='password_reset'),
    path('auth/password-reset/done/', base_auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^auth/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        base_auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('password_reset_complete'),), name='password_reset_confirm'),
    path('auth/reset/done/', base_auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # account management
    path('accounts/user/', UserViewSet.as_view({"get": "profile"}), name='profile'),  # deprecated, use user/profile
    path('accounts/register/', UserRegisterView.as_view(), name='register'),
    path('accounts/change-password/reset/<slug:uidb64>/<slug:token>/',
         UserSetPasswordView.as_view(), name='reset-password'),
    path('accounts/change-password/reset/', UserChangePasswordView.as_view(), name='new-password'),
    path('', include(router.urls))
]
