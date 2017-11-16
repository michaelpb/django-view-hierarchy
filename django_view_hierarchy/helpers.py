import re

from django.conf.urls import url
from contextlib import contextmanager

from django_view_hierarchy.decorators import add_breadcrumbs

GROUP_RE = re.compile(r'\(?P[^\)]+\)')

def _flatten_hierarchy(hierarchy, prefix=''):
    results = []
    for subpath, view_or_dict in hierarchy.items():
        path = ('%s/%s' % (prefix, subpath)).strip('/')
        regex_path = ('^%s/$' % path) if path else '^$'

        if isinstance(view_or_dict, dict):
            flat = _flatten_hierarchy(view_or_dict, prefix=path)
            results.extend(flat)
        else:
            results.append((regex_path, view_or_dict))

    # To make predictable re. ordering, always return alphabetically
    return sorted(results, key=lambda item: item[0])

def _wrap_view(parents, view):
    # TODO: Properly keep track of how deep each arg and kwarg we have
    parent_list = []
    for parent in parents:
        parent_list.append((parent, 43))
    return add_breadcrumbs(parent_list)(view)

def _generate_breadcrumb_hierarchy(hierarchy, parent_views=tuple(), count=0):
    results = {}

    for key, value in hierarchy.items():
        if key == '':
            parents = parent_views
        elif '' in hierarchy:
            parents = parent_views + (hierarchy[''], )

        # Count how many positional args are in each view
        total_group_count = count + len(GROUP_RE.findall(key))

        if isinstance(value, dict):
            # Recurse into subvalues, maintaining parent views
            results[key] = _generate_breadcrumb_hierarchy(
                value,
                parent_views=parents,
                count=total_group_count
            )
        else:
            results[key] = _wrap_view(parents, view)
    return results

def view_hierarchy(hierarchy):
    '''
    Given a dict structuring a hierarchy of views, produces an urlpatterns

    As an example:

    >>> def user_list(request): pass
    >>> def view_user(request, uid): pass
    >>> def user_history(request, uid): pass
    >>> urlpatterns = vh({
    ...     'users': {
    ...         '': user_list,
    ...         '(?P<uid>\d+)': {
    ...             '': user_view,
    ...             'activity': {
    ...                 user_view_activity,
    ...             },
    ...         },
    ...     },
    ... })
    >>> urlpatterns
    [
        url('^users/$', user_list),
        url('^users/(?P<uid>\d+)/$', user_view),
        url('^users/(?P<uid>\d+)/activity/$', user_view_activity),
    ]
    '''
    flattened = _flatten_hierarchy('', hierarchy)
    return [
        url(path, view) in flattened
    ]



