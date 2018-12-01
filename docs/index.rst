.. _index:

================================
WFP Django Temporary Permissions
================================

Django application to manage temporary permissions to the user's groups


Install
======================

configure your settings.py::

    INSTALLED_APPS = (
        ....,
        'django_temporary_permissions'
    )

    AUTHENTICATION_BACKENDS = (
        ....,
        'django_temporary_permissions.backends.TempPermissionsBackend',
    )

How to enable the management of the temporary permissions for the anonymous users
=================================================================================

To enable the management of the temporary permissions (disabled by default) for the anonymous users, configure your ``settings`` with ::

    TEMP_PERMISSIONS_MANAGE_ANONYMOUS_USER = True
    TEMP_PERMISSIONS_ANONYMOUS_USERID = 999

replace the TEMP_PERMISSIONS_ANONYMOUS_USERID value with the one assigned to the anonymous user into your database


Changelog
=========

.. toctree::
    :maxdepth: 2


    changes

