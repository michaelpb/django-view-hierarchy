from django.urls import reverse
from django.views import View


def get_info_from_cbv_instance(view):
    '''
    Given a Class Based View Instance, determine the title and URL.
    '''
    url = view.get_reverse_url()
    if view.breadcrumb:
        return str(view.breadcrumb), url
    return view.get_breadcrumb(), url


def get_info_from_view(view, request, args, kwargs):
    '''
    Given a regular function-based view and a request with args and kwargs,
    attempt to determine the breadcrumbs necessary.
    '''
    if view.breadcrumb:
        title = view.breadcrumb
    else:
        title = view.get_breadcrumb(request, *args, **kwargs)

    if view.view_name:
        url = reverse(view.view_name, args=args, kwargs=kwargs)
    else:
        url = reverse(view, args=args, kwargs=kwargs)
    return title, url


def get_info_from_view_or_cbv(view, request, args, kwargs):
    '''
    Given a view, which could either be an instanced or uninstanced Class
    Based View class, or regular flat view, determine the title and URL.
    '''

    if not hasattr(view, 'as_view') and not isinstance(view, View):
        # Simple functional view
        return get_info_from_view(view, request, args, kwargs)

    if not isinstance(view, View):  # Instance CBV first
        view = prep_cbv(view, request, kwargs, args)

    # Is an instanced
    return get_info_from_cbv_instance(view)


def prep_cbv(cls, request, kwargs, args):
    '''
    Given a Class Based View class, a request, and kwargs and args,
    instantiate it in the exact same way that View.as_view() instantiates
    it, prepping it with expected attributes (request, args, and kwargs).
    '''
    instance = cls()
    if hasattr(instance, 'get') and not hasattr(instance, 'head'):
        instance.head = instance.get
    instance.request = request
    instance.args = args
    instance.kwargs = kwargs
    return instance


def set_request_breadcrumbs(view_or_cbv, request, all_args, all_kwargs):
    '''
    Given a request to a view, and all positional and keyword arguments,
    processes request.breadcrumbs to contain info from all parent views.

    Assumes request.breadcrumbs
    '''
    bc_sources = request.breadcrumbs.bc_sources
    for view, arg_names in bc_sources:
        # The only requirement for breadcrumb enabled views is it must have
        # breadcrumb property (even if set to None)
        if not hasattr(view, 'breadcrumb'):
            raise ValueError('No breadcrumb for view: "%s"' % str(view))

        # Filter down positional and keyword args to only relevant ones
        arg_count = len(arg_names)
        args = all_args[:arg_count]
        kwargs = {
            key: value for key, value in all_kwargs.items()
            if key in arg_names
        }

        # Determine and append the breadcrumb title and reverse URL
        title, url = get_info_from_view_or_cbv(view, request, args, kwargs)
        request.breadcrumbs.append(title, url, view.breadcrumb_groups)

    # Finally, append current breadcrumb
    title, url = get_info_from_view_or_cbv(
        view_or_cbv, request, all_args, all_kwargs)
    request.breadcrumbs.append(title, url, view_or_cbv.breadcrumb_groups)
