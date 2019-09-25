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
