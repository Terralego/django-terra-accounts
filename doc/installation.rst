Installation
============

Requirements
------------

Minimum configuration :
 * Postgresql 10

Recommended configuration :
 * Postgresql 11

Your final django project should use postgresql or postgis as default DATABASE backend


USING docker image :

Prebuilt docker image builded by makinacorpus

https://cloud.docker.com/u/makinacorpus/repository/docker/makinacorpus/pgrouting/general


With pip
--------

From Pypi:

::

    pip install django-terra-accounts

From Github:

::

    pip install -e https://github.com/Terralego/django-terra-accounts.git@master#egg=django-terra-accounts

With git
--------

::

    git clone https://github.com/Terralego/django-terra-accounts.git
    cd django-terra-accounts
    python setup.py install
