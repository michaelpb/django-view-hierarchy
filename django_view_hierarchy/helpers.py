import re

from django.conf.urls import url

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


def _wrap_view(parent_views, view):
    if not hasattr(view, 'breadcrumb'):
        view.__name__
        raise ValueError('Invalid view: %s' % view.__name__)

    if hasattr(view, 'as_view'):
        # Is a class based view, call as_view first
        wrapped_view = add_all_breadcrumbs(parent_views)(view.as_view())
    else:
        # Is a classic functional view, be sure to add breadcrumbs too
        wrapped_view = add_all_breadcrumbs(parent_views, True)(view)

    # Set up view_name with default and return
    if not view.view_name:
        view.view_name = view.__name__
    wrapped_view._view_name = view.view_name

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
    '''
    wrapped_hierarchy = _generate_breadcrumb_hierarchy(hierarchy)
    flattened = _flatten_hierarchy(wrapped_hierarchy)
    return [
        url(path, view, name=view._view_name) for path, view in flattened
    ]
