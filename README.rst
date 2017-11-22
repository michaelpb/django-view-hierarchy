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

Hierarchical view system Python Django. Define an arbitrary hierarchical
URL structure in your ``urls.py``, define how breadcrumbs get generated for
each view, and then this package will automatically generate breadcrumbs
attached to the request object that can be easily rendered in any page, to
easily link "up" the view hierarchy.

Features
------------

* Supports both Class Based Views and simple functional views

* Auto-generates an ``urlpatterns`` for any nested URL pattern, keeping
  your ``urlpatterns`` more DRY

* Automatically generates breadcrumbs with both title and URL available as
  ``request.breadcrumbs`` for each node in ancestor tree


Quick start
------------

**Overview:**

1. Install django_view_hierarchy and put in requirements file
2. Add to INSTALLED_APPS
3. Create a view hierarchy with one or more

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

3. Use decorator or mixin to add view hierarchy to views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For Class Based Views, do the following:

.. code-block:: python

    from django.views import View
    from django_view_hierarchy.views import BreadcrumbMixin

    class UserList(BreadcrumbMixin, View):
        breadcrumb = 'All users'    # Static

For more complicated examples, you may need to specify a breadcrumb that
involves fetching data from the DB or giving your view a name:

.. code-block:: python
    class UserDetailView(BreadcrumbMixin, View):
        view_name = 'user_details'  # Optionally give view a name
        def get_breadcrumb(self):
            pk = self.kwargs['pk']
            user = User.objects.get(pk=pk)
            return user.username

For function-style views, you can do the same thing as follows:

.. code-block:: python
    from django_view_hierarchy.decorators import breadcrumb

    @breadcrumb('Users')
    def user_list_view(request):
        return render_to_response('...')

    @breadcrumb(lambda request, pk: User.objects.get(pk).username, 'user_details')
    def user_detail_view(request, pk):
        return render_to_response('...')


4. Configure hierarchy in urls.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For example, to make a set of views like:

* ``/users/``  for a list of all users
* ``/users/<userid>/``  for a particular user
* ``/users/<userid>/followers/``  for a sub-page of a particular user,
  showing off their followers

The hierarchy can be built like:

.. code-block:: python
    from django_view_hierarchy.helpers import view_hierarchy
    urlpatterns = view_hierarchy({
        'users': {
            '': UserListView,
            '(?P<pk>\d+)': {
                '': UserDetailView,
                'followers': user_followers_view,
            },
        },
    })

Note that Class Based Views *should not* include `as_view`, this will be
done automatically.


5. Use breadcrumbs in views and/or templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: html

    <ul>
        {% for breadcrumb in request.breadcrumbs %}
            <li>
                <a href="{{ breadcrumb.url }}">{{ breadcrumb.title }}</a>
            </li>
        {% endfor %}
    </ul>


Credits
-------

Tools used in creating this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
