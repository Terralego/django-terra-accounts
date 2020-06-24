
CHANGELOG
=========

0.3.11         (2020-06-24)
----------------------------

* Fix settings override by TERRA_APPLIANCE_SETTINGS

0.3.10          (2020-06-03)
----------------------------

* Move settings endpoint from terra_utils
* Serve language from instance defined language

0.3.9           (2020-03-20)
----------------------------

* Manage reset password views


0.3.8           (2019-12-13)
----------------------------

* Update documentation
* Support Django 3.0
* Support DjangoRestFramework 3.11


0.3.7.1         (2019-11-26)
----------------------------

* Include inherited permissions from groups to user
* Improve Terra Permission creation


0.3.6      (2019-11-05)
----------------------------

* Add a method to check if a user has some terra permission

0.3.5      (2019-11-04)
----------------------------

* Implement TerraPermissions

0.3.4      (2019-10-08)
----------------------------

* Deprecate looking up user by id (will be removed in 0.4.0)

0.3.3      (2019-10-03)
-----------------------

### Feature

* test factories are now included in packaging


0.3.2      (2019-09-27)
-----------------------

### Fixes

* Groups must be a DRF standard attribute


0.3.1      (2019-09-26)
-----------------------

### Fixes

* Fix id in Group serializer (and API)


0.3.0      (2019-09-25)
-----------------------

### Breaking Changes

* App name move from accounts to terra_accounts. Structure is the same, so backup and restore your data

First public tag

* Terra app extracted from terracommon.accounts
