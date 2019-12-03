[![Build Status](https://travis-ci.org/Terralego/django-terra-accounts.svg?branch=master)](https://travis-ci.org/Terralego/django-terra-accounts)
[![codecov](https://codecov.io/gh/Terralego/django-terra-accounts/branch/master/graph/badge.svg)](https://codecov.io/gh/Terralego/django-terra-accounts)
[![Maintainability](https://api.codeclimate.com/v1/badges/0dbea745485facded80a/maintainability)](https://codeclimate.com/github/Terralego/django-terra-accounts/maintainability)

# django-terra-accounts

Django accounts management for terralego apps

https://django-terra-accounts.readthedocs.io/

## WARNING

* splitted from terracommon.accounts

* If you want to migrate data, please :
  * test in local env
    * all terracommon.accounts reference should be replaced by terra_accounts
    * all migration file which is referencing a 'accounts' migration should reference 'terra_accounts'
  * backup your instance
  * stop instance
  * update your django_content_type table
    * UPDATE django_content_type SET app_label = 'terra_accounts' WHERE app_label = 'account';
  * update your django_migrations table
    * UPDATE django_migrations SET app = 'terra_accounts' WHERE app = 'account';
  * Rename tables
      * ALTER TABLE accounts_terrauser RENAME TO terra_accounts_terrauser;
      * ALTER TABLE accounts_readmodels RENAME TO terra_accounts_readmodel;
  * Restart instances and launch migrations

## Setting Up

It's recommended to follow all instruction if you don't know how this app really works, else if you set up half of this, you may experience
some problems.

### Django app and URLs

If you plan to use User API for authentication, registration, and other this, you should add the `terra_accounts` app to INSTALLED_APPS and

```
INSTALLED_APPS = (
  [...],
  'terra_accounts',
)
```

And include terra_accounts's URLs to your project urls, by adding this:
```
path("", include("terra_accounts.urls")),
```


### User's model

To set up the Terra User Model, you should follow the standard django procedure, by adding this to you project settings:
```
AUTH_USER_MODEL = 'terra_accounts.TerraUser'
```

### Payload handler

You should also override the default payload handler of jwt tokens, setting this:
```
JWT_AUTH = {
  'JWT_PAYLOAD_HANDLER' 'terra_accounts.jwt_payload.terra_payload_handler',
}
```


### Permissions mixin

If you plan to use the permission mecanism which heritate from django Permission class you should add the permission mixin
to your appconfig's.

There is an exemple of AppConfig
```
from django.apps import AppConfig

from terra_accounts.permissions_mixins import PermissionRegistrationMixin


class MyAppConfig(PermissionRegistrationMixin, AppConfig):
    name = 'my_app'

    permissions = (
        ('can_do_something', 'Is able to do something'),
        ('can_do_whatever', 'Is able to do whatever'),
    )
```

The permission mixin, overrides the `ready()` method to register a signal. If you plan to override this method, do not
forget to add a call to `super().ready()`


## To start a dev instance

Define settings you wants in `test_geosource` django project.

```sh
docker-compose up
```

First start should failed as the database need to be initialized. Just launch
the same command twice.

Then initialize the database:

```sh
docker-compose run web /code/venv/bin/python3 /code/src/manage.py migrate
```

You can now edit your code. A django runserver is launched internally so the
this is an autoreload server.

You can access to the api on http://localhost:8000/api/


## Test

To run test suite, just launch:

```sh
docker-compose run web /code/venv/bin/python3 /code/src/manage.py test
```
