=============================
Django DjangoViewHiearchy
=============================

.. image:: https://img.shields.io/pypi/v/django_view_hierarchy.svg
    :target: https://pypi.python.org/pypi/django_view_hierarchy/

.. image:: https://travis-ci.org/michaelpb/django_view_hierarchy.svg?branch=master
    :target: https://travis-ci.org/michaelpb/django_view_hierarchy

.. image:: https://codecov.io/gh/michaelpb/django_view_hierarchy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/michaelpb/django_view_hierarchy

* **NOTE:** Presently *only* supports Python 3.5+ and Django 1.9+ (see `issue
  #1 <https://github.com/michaelpb/django_view_hierarchy/issues/1>`_)

Activity stream for Python Django. Unlike other activity streams, it is much
more flexible, with every event designed to supporting an arbitrary number of
associated objects. It also is designed to be unobtrusive: Any of your models
can be registered as an activity generator, all you need to do is generate a
data structure for context, or an HTML fragment.

Features
--------

- Very easily / magically integrated into an existing system, with signals
  being auto-generated based on principle objects
- Arbitrary number of objects can be associated with every event
- Fast look ups with denormalized events (no joins)
- Looking up streams for particular actors or objects
- Decent test coverage
- Handy Paginator helper class to page through stream
- Example project

- **Not yet implemented:** Follow


Quick start
------------

**Overview:**

1. Install django_view_hierarchy and put in requirements file
2. Add to INSTALLED_APPS
3. Pick several important models to implement the django_view_hierarchy interface so that every save or update generates an event
4. Add those models to ACTABLE_MODELS
5. Use helper classes to add a streams to your views

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

3. Implement DjangoViewHiearchy interface in one or more models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pick one or more models to be your django_view_hierarchy models. Whenever these models are
updated or created, it will generate events. These events can involve any
number of other objects.

To implement the required interface, you must implement at least 2 methods on
your django_view_hierarchy models. The first method is ``get_django_view_hierarchy_relations`` which must
return a dictionary where all the values are model instances that are related
to this action.  Instead of limiting yourself to "Actor, Verb, Object", this
allows you to have any number of relations.  Each one of these model instances
will receive a copy of this event to its activity stream.

Example:

.. code-block:: python

    class ProjectBlogPost:
        def get_django_view_hierarchy_relations(self, event):
            return {
                'subject': self.user,
                'object': self,
                'project': self.project,
            }

Now you must choose one of 2 other methods to implement. These constitute the
data to cache for each event.

The most versatile of the two is one that returns a dictionary containing
entirely simple (serializable) data types. This will be stored in serialized
form in your database.

Example:

.. code-block:: python

    class ProjectBlogPost:
        def get_django_view_hierarchy_json(self, event):
            verb = 'posted' if event.is_creation else 'updated'
            return {
                'subject': self.user.username,
                'subject_url': self.user.get_absolute_url(),
                'object': self.title,
                'object_url': self.get_absolute_url(),
                'project': self.project.title,
                'verb': verb,
            }


The other option is caching an HTML snippet (string) that can be generated any
way you see fit.

Example:

.. code-block:: python

    class ProjectBlogPost:
        def get_django_view_hierarchy_html(self, event):
            return '<a href="%s">%s</a> wrote %s' % (
                self.user.get_absolute_url(),
                self.user.username,
                self.title
            )


4. Add to ACTABLE_MODELS list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, you should list your newly improved as an ``ACTABLE_MODEL``, as such:

.. code-block:: python

    ACTABLE_MODELS = [
        'myapp.ProjectBlogPost',
    ]


5. Include stream in your views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In your views, you can use the EventDictPaginator to easily include streams.
This will fetch streams relveant to any given model specified as an "django_view_hierarchy
relation" (that is, it works on more models than just the ``ACTABLE_MODELS``)

Example:

.. code-block:: python

    from django_view_hierarchy.helpers import EventDictPaginator
    ...

    def view_user(request, username):
        user = User.objects.get(username=username)
        event_paginator = EventDictPaginator(user, 50)
        return render(request, 'userpage.html', {
            stream: event_paginator.page(request.get('page', 1)),
        })

EventDictPaginator will consist of de-serialized dicts, exactly as you
generated them in ``get_django_view_hierarchy_json``, with one added property ``date``, which
will be a Python ``datetime`` for the event.

Other helpers
-------------

For more descriptive activity items in the style of 'Alice updated the blog
post title from "2018 Plans" to "2018 goals"', there is a helper to
detect changes between two versions of

.. code-block:: python
    from django_view_hierarchy.helpers import ModelChangeDetector

    post = ProjectBlogPost.objects.create(title='2018 Plans')
    changes = ModelChangeDetector(post)
    post.title = '2018 goals'
    changes.get_editable_changes(title)
    # Will return: {'title': ('2018 Plans', '2018 goals')}


Credits
-------

Tools used in creating this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
