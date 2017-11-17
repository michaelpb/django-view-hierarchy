import re

from django.conf.urls import url
from contextlib import contextmanager

from django_view_hierarchy.decorators import add_all_breadcrumbs

GROUP_RE = re.compile(r'\(?P<(\w+)>[^\)]+\)')

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

def _wrap_view(parents, original_view):
    # TODO: Properly keep track of how deep each arg and kwarg we have
    # Once tested, refactor To not loop through parents
    parent_list = []
    #import code;_g=globals();_g.update(locals());code.InteractiveConsole(_g).interact();
    for parent, arg_names in parents:
        parent_list.append((parent, arg_names))

    view = None
    if hasattr(original_view, 'as_view'):
        # Is a class based original_view
        view = original_view.as_view()
    else:
        raise ValueError('Only CBV presently supported: %s' % str(view))

    # Wrap view with the add_all_breadcrumbs helper
    wrapped_view = add_all_breadcrumbs(parent_list)(view)
    original_view._plain_view = wrapped_view

    # Set up view name variables
    if original_view.view_name is None:
        view_name = original_view.__name__
        original_view.view_name = view_name
    else:
        view_name = original_view.view_name
    wrapped_view._view_name = view_name

    # Return prepped wrapped view
    return wrapped_view

def _generate_breadcrumb_hierarchy(hierarchy, views=tuple(), args=tuple()):
    results = {}

    for key, view in hierarchy.items():
        parents = views
        if key == '':
            pass  # Doesn't actually add anything, parents is this one
        elif '' in hierarchy:
            pair = (hierarchy[''], args)
            parents = views + (pair, )

        # args how many positional args are in each view
        all_args = args + tuple(GROUP_RE.findall(key))

        if isinstance(view, dict):
            # Recurse into subvalues, maintaining parent views
            results[key] = _generate_breadcrumb_hierarchy(
                view,
                views=parents,
                args=all_args,
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
    wrapped_hierarchy = _generate_breadcrumb_hierarchy(hierarchy)
    flattened = _flatten_hierarchy(wrapped_hierarchy)
    return [
        url(path, view, name=view._view_name) for path, view in flattened
    ]

