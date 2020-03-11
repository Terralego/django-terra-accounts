Configuration
=============


In your project :

# settings
::
    # install required apps
    INSTALLED_APPS = [
        ...
        # required apps to work with terra_accounts
        'rest_framework',
        'rest_framework_jwt',
        'terra_utils',
        # terra_accounts app
        'terra_accounts',
        ...
    ]

    TERRA_USER_STRING_FORMAT = ''  # python doted path to function that return user string formatted

# urls
::

    urlpatterns = [
        ...
        # required apps to work with terra_accounts
        path('', include('terra_utils.urls', namespace='terra_utils')),
        # terra_accounts app
        path('', include('terra_accounts.urls', namespace='terra_accounts')),
        ...
    ]

You can customize default url and namespace by including terra_accounts.views directly


# ADMIN :

you can disable and / or customize admin


- BACKWARD compatibility

# Password reset

* you must set settings to correctly generate and send email for password reset.

  * FRONT_URL : default to http://localhost:3000 . Should match with your front url
  * Other settings to send mails ->
  * https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-EMAIL_HOST
