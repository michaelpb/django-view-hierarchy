from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url

from .middleware import BreadcrumbList

class Breadcrumb(namedtuple('Breadcrumb', ['title', 'url'])):
    def __str__(self):
        return '<a href="%s">%s</a>' % (
            self.url,
            self.title,
        )

class BreadcrumbList:
    def __init__(self):
        self.bc_sources = []

    def append(self, title, url):
        super().append(Breadcrumb(title, url))

    def add_breadcrumb_source(self, view, arg_count):
        self.bc_sources.append((view, arg_count))

def add_breadcrumbs(parent_views):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            request.breadcrumbs = BreadcrumbList()
            for view, arg_count in parent_views:
                request.breadcrumbs.add_breadcrumbs(view, arg_count)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

