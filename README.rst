=============================
Django DjangoViewHiearchy
=============================

.. image:: https://img.shields.io/pypi/v/django_view_hierarchy.svg
    :target: https://pypi.python.org/pypi/django_view_hierarchy/

.. image:: https://travis-ci.org/michaelpb/django_view_hierarchy.svg?branch=master
    :target: https://travis-ci.org/michaelpb/django_view_hierarchy

.. image:: https://codecov.io/gh/michaelpb/django_view_hierarchy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/michaelpb/django_view_hierarchy

* **WIP:** This app is still being developed and documented! Use at your
  own risk.

* **NOTE:** Presently *only* supports Python 3.5+ and Django 1.9+ (see `issue
  #1 <https://github.com/michaelpb/django_view_hierarchy/issues/1>`_)

Hierarchical view system Python Django.

Provides a set of helpers for constructing meaningful hierarchical Class Based
Views, and context processes for very easily including breadcrumbs, tabs, etc
in the templates.

Quick start
------------

**Overview:**

1. Install django_view_hierarchy and put in requirements file
2. Add to INSTALLED_APPS
3. TODO

---------------

1. Install
~~~~~~~~~~


.. code-block:: bash

    pip install django_view_hierarchy

2. Add to INSTALLED_APPS
~~~~~~~~~~~~~~~~~~~~~~~~

In your ``settings.py`` file, add something like:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_view_hierarchy.apps.DjangoViewHiearchyConfig',
        ...
    )

3. Implement DjangoViewHiearchy interface in one or urls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO

Credits
-------

Tools used in creating this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
