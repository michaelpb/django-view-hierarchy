from collections import namedtuple
from functools import wraps

from django_view_hierarchy.utils import set_request_breadcrumbs

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

    @property
    def last(self):
        if len(self) < 1:
            return None
        return self.breadcrumbs[-1]

    @property
    def first(self):
        if len(self) < 1:
            return None
        return self.breadcrumbs[0]

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

            # If view_func came from a decorated simple view function as
            # opposed to a CBV, need to add breadcrumbs now
            if also_set_breadcrumbs:
                set_request_breadcrumbs(view_func, request, args, kwargs)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def breadcrumb(breadcrumb_getter, view_name=None):
    '''
    Given a string or a function which takes the same sort of arguments as
    the view, and optionally a view name, wrap the current view in a way
    that will append as needed breadcrumbs to the breadcrumbs object. This
    assumes the view has already been inserted in a view hierarchy.
    '''
    def decorator(view_func):
        view_func.breadcrumb = None
        view_func.view_name = view_name
        if isinstance(breadcrumb_getter, str):
            view_func.breadcrumb = breadcrumb_getter
        else:
            view_func.get_breadcrumb = breadcrumb_getter
        return view_func
    return decorator

