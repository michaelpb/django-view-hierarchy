from collections import namedtuple
from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.urls import reverse

class Breadcrumb(namedtuple('Breadcrumb', ['title', 'url'])):
    def __str__(self):
        return '<a href="%s">%s</a>' % (
            self.url,
            self.title,
        )

class BreadcrumbList:
    def __init__(self):
        self.bc_sources = []
        self.breadcrumbs = []

    def append(self, title, url):
        self.breadcrumbs.append(Breadcrumb(title, url))

    def add_breadcrumb_source(self, view, arg_names):
        self.bc_sources.append((view, arg_names))

    def __len__(self):
        return len(self.breadcrumbs)

    def __iter__(self):
        return iter(self.breadcrumbs)

def add_all_breadcrumbs(parent_views, also_set_breadcrumbs=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            request.breadcrumbs = BreadcrumbList()
            for view, arg_names in parent_views:
                request.breadcrumbs.add_breadcrumb_source(view, arg_names)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# TODO To give the option of non-CBV views, add breadcrumb decorator to
# attach either strings or callables to views and allows for arbitrary
# functions to generate breadcrumbs for views. Something like this:
def breadcrumb(breadcrumb_getter, view_name=None):
    def decorator(view_func):
        view_func.breadcrumb = None
        view_func.view_name = view_name
        if isinstance(breadcrumb_getter, str):
            view_func.breadcrumb = breadcrumb_getter
        else:
            view_func.get_breadcrumb = breadcrumb_getter
        return view_func
    return decorator

