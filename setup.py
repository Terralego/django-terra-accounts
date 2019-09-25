#!/usr/bin/env python

import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(HERE, 'README.md')).read()
CHANGES = open(os.path.join(HERE, 'CHANGES.md')).read()


setup(
    name='django-terra-accounts',
    version=open(os.path.join(HERE, 'terra_accounts', 'VERSION.md')).read().strip(),
    include_package_data=True,
    author="Makina Corpus",
    author_email="terralego-pypi@makina-corpus.com",
    description='Django accounts management for terralego apps',
    long_description=README + '\n\n' + CHANGES,
    description_content_type="text/markdown",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url='https://github.com/Terralego/django-terra-accounts.git',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'django>=2.2,<3.1',
        'psycopg2>=2.7',  # postgres is required to use JSONField
        'django-terra-utils>=0.3.5',
        'djangorestframework>=3.8',
        "djangorestframework-jwt>=1.11",
        "django-url-filter>=0.3",
    ],
    extras_require={
        'dev': [
            'factory-boy',
            'flake8',
            'coverage',
        ]
    }
)
