#!/usr/bin/env python
import codecs
import os
from distutils.config import PyPIRCCommand

from setuptools import find_packages, setup

dirname = 'django_temporary_permissions'

app = __import__(dirname)


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()


PyPIRCCommand.DEFAULT_REPOSITORY = 'https://pypi.org/'

tests_require = read('%s/requirements/testing.pip' % dirname)

setup(
    name=app.NAME,
    version=app.get_version(),
    url='https://pypi.org/project/%s/' % app.NAME,
    author='Matteo Cafarotti',
    author_email='m.cafarotti@gmail.com',
    license="Free",
    description='Django Temporary Permissions Library',
    long_description=read('README'),
    packages=find_packages(exclude=['tests', 'docs', 'demo']),
    include_package_data=True,
    dependency_links=['https://pypi.org/', ],
    install_requires=read('django_temporary_permissions/requirements/install.pip'),
    tests_require=tests_require,
    test_suite='conftest.runtests',
    extras_require={
            'tests': tests_require,
    },
    platforms=['linux'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers'
    ]
)
